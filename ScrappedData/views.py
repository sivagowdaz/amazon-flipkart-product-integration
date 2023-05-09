from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models.expressions import F, OrderBy
from django.shortcuts import render
from django.contrib.auth.models import User
from . models import FlipkartData, AmezonData, PdfFiles

import os
import re
from django.conf import settings

from fpdf import FPDF
import requests

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView


from bot.run import call_thread, login_to_amazon, login_to_flipkart


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('query_page')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return super(RegisterPage, self).form_valid(form)

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return redirect('login')
    #     return super(RegisterPage, self).get(*args, **kwargs)


def string_filter(string):
    return ''.join([i for i in string if ord(i) < 256])


amazon_products = []
flipkart_products = []
search_string = 'Search'


def query_page(request):
    print('page is refreshed')
    if not request.user.is_authenticated:
        return redirect('login')

    global search_string
    global flipkart_products
    global amazon_products

    new_search_string = request.POST.get('search_string')
    print("old", search_string)
    print("new", new_search_string)
    if new_search_string and new_search_string != search_string and new_search_string != 'Search':
        search_string = new_search_string
        print("updated", search_string)
        # amazon_products = amazon_function(search_string)
        # flipkart_products = flipkart_function(search_string)
        amazon_products, flipkart_products = call_thread(search_string)
    print("Amazon and Flipkart products", amazon_products)
    print('last', search_string)

    if request.POST.get('index_value_f') and len(flipkart_products) != 0:
        index = request.POST.get('index_value_f')
        print("the index is", index)
        print('len of', len(flipkart_products))
        required_data = flipkart_products[int(index)]
        if required_data["product_description"]:
            new_product_description = '|'.join(
                required_data["product_description"])
        else:
            new_product_description = 'not available'
        new_product = FlipkartData.objects.create(
            user=request.user,
            image=required_data["product_image"],
            title=required_data["product_heading"],
            ratting=required_data["product_ratting"],
            review_data=required_data["user_review_text"],
            price=required_data["price_of_product"],
            discount=required_data["discount_percentage"],
            original_price=required_data["original_price"],
            product_description=new_product_description,
            product_link=required_data["product_url"]
        )
        new_product.save()
    if request.POST.get('index_value_a') and len(amazon_products) != 0:
        index = request.POST.get('index_value_a')
        print("the index is", index)
        required_data = amazon_products[int(index) - 100]
        new_product = AmezonData.objects.create(
            user=request.user,
            image=required_data["product_image"],
            ratting=required_data["ratting"],
            review_num=required_data["total_review"],
            price=required_data["product_price"],
            product_description=required_data["product_description"],
            product_link=required_data["product_link"]
        )

        new_product.save()
    res_file = None
    # try:
    # if (request.POST.get('downloader')):
    #     PdfFiles.objects.all().delete()
    #     path = os.path.join(settings.MEDIA_ROOT,
    #                         "pdf_files", "product_detail.txt")
    #     fh = open(path, 'wb')
    #     fh.truncate()
    #     data = request.POST.get('downloader')
    #     print(data)
    #     newdata = data.split("&")
    #     for data in newdata:
    #         id = data.split('-')[0]
    #         id = id.strip()

    #         if int(id)<99:
    #             print(flipkart_products[int(id)])
    #             product = flipkart_products[int(id)]
    #             print(product)
    #             data = f"{product['product_heading']}\nratting: {product['product_ratting']}\nreview data:{product['user_review_text']}\nprice: {product['price_of_product']}\ndescount price:{product['discount_percentage']}\noriginal price:{product['original_price']}\nproduct description:\n{product['product_description'][0]}\n{product['product_description'][1]}\n{product['product_description'][2]}\n{product['product_description'][3]}\n-------------------------\n".encode(
    #                 encoding='UTF-8')
    #             print(data)
    #             fh.write(data)
    #         else:
    #             print(amazon_products[int(id)-100])
    #             product = amazon_products[int(id)-100]
    #             data = f"{product['product_description']}\nratting:{product['ratting']}\n{product['total_review']}\nprice: {product['product_price']}\n-------------------------\n".encode(
    #                 encoding='UTF-8')
    #             print(data)
    #             fh.write(data)
    #     fh.close()
    #     print('above')
    #     file = PdfFiles()
    #     file.pdf_file.name = path
    #     file.save()

    #     res_file = PdfFiles.objects.all()[0]

    #     print("bellow")
    if (request.POST.get('downloader')):
        PdfFiles.objects.all().delete()
        path = os.path.join(settings.MEDIA_ROOT,
                            "pdf_files", "product_detail.pdf")

        pdf = FPDF()
        count = 0
        line_num = 1
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        data = request.POST.get('downloader')
        print(data)
        newdata = data.split("&&&&")
        for data in newdata:
            id = data.split('-')[0]
            id = id.strip()
            print("the id is ", id)

            if int(id) < 99:
                product = flipkart_products[int(id)]
                file_name = None
                if product['product_image'] != '#':
                    image = requests.get(product['product_image']).content
                    file_name = f"{'image' + str(id)}.jpg"
                    image_file = open(file_name, 'wb')
                    image_file.write(image)
                    image_file.close()
                    pdf.image(file_name)
                if product['product_heading']:
                    pdf.cell(
                        10, 5, txt=product["product_heading"], ln=line_num, align='c')
                    line_num += 1
                if product['product_ratting']:
                    pdf.cell(
                        10, 5, txt=product["product_ratting"], ln=line_num, align='c')
                    line_num += 1
                if product['user_review_text']:
                    pdf.cell(
                        10, 5, txt=product["user_review_text"], ln=line_num, align='c')
                    line_num += 1
                if product['price_of_product']:
                    modified_price = product["price_of_product"][1:]
                    pdf.cell(10, 5, txt=modified_price, ln=line_num, align='c')
                    line_num += 1
                if product['original_price']:
                    modified_or_price = product["original_price"][1:]
                    pdf.cell(10, 5, txt=modified_or_price,
                             ln=line_num, align='c')
                    line_num += 1
                if product['discount_percentage']:
                    pdf.cell(
                        10, 5, txt=product["discount_percentage"], ln=line_num, align='c')
                    line_num += 1
                if product['product_description']:
                    pdf.cell(10, 5, txt='product description:',
                             ln=line_num, align='c')
                    line_num += 1
                    for des in product["product_description"]:
                        pdf.cell(10, 5, txt=des, ln=line_num, align='c')
                        line_num += 1
                if file_name:
                    if os.path.exists(file_name):
                        os.remove(file_name)
                count += 1
            else:
                product = amazon_products[int(id)-100]
                if product['product_image']:
                    image = requests.get(product['product_image']).content
                    file_name = f"{'image' + str(id)}.jpg"
                    image_file = open(file_name, 'wb')
                    image_file.write(image)
                    image_file.close()
                    pdf.image(file_name)

                if product['product_description']:
                    desc_array = product['product_description'].split(',')
                    for desc in desc_array:
                        pdf.cell(10, 5, txt=desc, ln=line_num, align='c')
                        line_num += 1
                if product['ratting']:
                    pdf.cell(
                        10, 5, txt=product["ratting"], ln=line_num, align='c')
                    line_num += 1
                if product['total_review']:
                    pdf.cell(
                        10, 5, txt=product["total_review"], ln=line_num, align='c')
                    line_num += 1
                if product['product_price']:
                    pdf.cell(
                        10, 5, txt=product["product_price"], ln=line_num, align='c')
                    line_num += 1
                if os.path.exists(file_name):
                    os.remove(file_name)
                count += 1
        pdf.output(path)
        file = PdfFiles()
        file.pdf_file.name = path
        file.save()
        res_file = PdfFiles.objects.all()[0]

    # except Exception as ex:
    #     print('inside the except')
    #     print(ex)
    email = None
    password = None
    product_identifier = None
    if request.POST:
        if request.POST.get('fproductid'):
            print("inside the dfjdkjfkdkfjdkj")
            if request.POST.get('femail'):
                email = request.POST.get('femail')
            if request.POST.get('fpassword'):
                password = request.POST.get('fpassword')
            product_identifier = request.POST.get('fproductid')

            print("the details are", email, password, product_identifier)

            if email and password and product_identifier:
                required_data_login = flipkart_products[int(
                    product_identifier)]
                identifier_text = required_data_login["product_heading"]
                login_to_flipkart(
                    email, password, search_string, identifier_text)

        if request.POST.get('aproductid'):
            if request.POST.get('aemail'):
                email = request.POST.get('aemail')
            if request.POST.get('apassword'):
                password = request.POST.get('apassword')
            product_identifier = request.POST.get('aproductid')

            print("the details are", email, password, product_identifier)

            if email and password and product_identifier:
                required_data_login = amazon_products[int(
                    product_identifier) - 100]
                identifier_text = required_data_login["product_description"]
                login_to_amazon(email, password,
                                search_string, identifier_text)

    if request.POST.get('fsort'):
        sort_string = request.POST.get('fsort')
        regex = re.compile(rf"{sort_string}", re.IGNORECASE)
        print("the sort string is", sort_string)
        sorted_flipkart_products = [
            product for product in flipkart_products if regex.search(product['product_heading'])]
    else:
        sorted_flipkart_products = flipkart_products

    if request.POST.get('asort'):
        sort_string = request.POST.get('asort')
        regex = re.compile(rf"{sort_string}", re.IGNORECASE)
        sorted_amazon_products = [
            product for product in amazon_products if regex.search(product['product_description'])]
    else:
        sorted_amazon_products = amazon_products

    stuff_for_frontend = {
        "amazon_products": sorted_amazon_products,
        "flipkart_products": sorted_flipkart_products,
        "search_string": search_string,
        "file_generated": res_file
    }

    return render(request, 'querypage.html', stuff_for_frontend)


def saved_for_later(request):
    flipkart_products = FlipkartData.objects.filter(user=request.user)
    amazon_products = AmezonData.objects.filter(user=request.user)

    if request.POST.get('f_id'):
        id = request.POST.get('f_id')
        print('the id is', id)
        try:
            to_be_deleted = FlipkartData.objects.get(id=id)
            to_be_deleted.delete()
        except:
            pass
    if request.POST.get('a_id'):
        id = request.POST.get('a_id')
        print('the id is', id)
        try:
            to_be_deleted = AmezonData.objects.get(id=id)
            to_be_deleted.delete()
        except:
            pass

    stuff_for_fontend = {
        "flipkart_products": flipkart_products,
        "amazon_products": amazon_products
    }

    return render(request, 'savedproduct.html', stuff_for_fontend)


def pagelogout(request):
    if request.method == "POST":
        logout(request)

        return redirect('login')
    else:
        print("something went wrong")
