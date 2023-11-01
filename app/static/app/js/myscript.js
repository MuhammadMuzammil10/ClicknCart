$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 3,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.pswp__caption__center').hide()

$(".plus-cart").click(function () {
    console.log("Plus Button Clicked")
    var id = $(this).attr("pid").toString()
    elem = this.parentNode.children[1]
    eleme = $(this).parent().parent().parent().next().children()[0]
    prod_id = id
    $.ajax({
        type: "GET",
        url: "/plus_cart/",
        data: { prod_id: id },
        beforeSend: function () {
            $('#cover-spin').show(0)
        },
        success: function (data) {
            $('#cover-spin').hide(0)
            ides = document.querySelector('#item' + id)
            document.querySelector('#count').innerText = data.data.count
            document.querySelector('.totalAmount').innerText = `Rs ${data.data.totalAmount}`
            counpon_div = document.querySelector('.coupon_discount')
            if (counpon_div) {
                ccounpon_div.innerText = `- Rs ${data.data.coupon_discount}`
            }
            ides.innerText = data.data.quantity
            eleme.innerText = `Rs: ${data.data.per_price}`
            elem.innerText = data.data.quantity
            console.log(eleme.innerText)
            t = document.querySelectorAll('.Subtotal')
            t.forEach(element => {
                element.innerText = `Rs: ${data.data.amount}`
            });
            document.getElementById('shipping_amount').innerText = data.data.shipping
        }
    })
})

$(".minus-cart").click(function () {
    console.log("Minus Button Clicked")
    var id = $(this).attr("pid").toString()
    elem = this.parentNode.children[1]
    eleme = $(this).parent().parent().parent().next().children()[0]
    prod_id = id
    $.ajax({
        type: "GET",
        url: "/minus_cart/",
        data: { prod_id: id },
        beforeSend: function () {
            $('#cover-spin').show(0)
        },
        success: function (data) {
            $('#cover-spin').hide(0)
            if (data.data.quantity >= 0) {
                ides = document.querySelector('#item' + id)
                document.querySelector('#count').innerText = data.data.count
                document.querySelector('.totalAmount').innerText = `Rs ${data.data.totalAmount}`
                counpon_div = document.querySelector('.coupon_discount')
                if (counpon_div) {
                    ccounpon_div.innerText = `- Rs ${data.data.coupon_discount}`
                }
                console.log(document.querySelector('.totalAmount').innerText)
                ides.innerText = data.data.quantity
                eleme.innerText = `Rs: ${data.data.per_price}`
                elem.innerText = data.data.quantity
                console.log(eleme.innerText)
                t = document.querySelectorAll('.Subtotal')
                t.forEach(element => {
                    element.innerText = `Rs: ${data.data.amount}`
                });
                document.getElementById('shipping_amount').innerText = data.data.shipping
            }
        }
    })
})

$(document).on('click', '.addtowishlist', function () {
    console.log('AddToCart Clicked')
    prod_id = $(this).attr('pid').toString()
    var $this = $(this); 
    $.ajax({
        type: "GET",
        url: "/add-to-wishlist/",
        data: { prod_id: prod_id },
        beforeSend: function () {
            $('.addtowishlist').attr('disabled', true);
        },
        success: function (data) {
            console.log(data)
            ref = data.data.product[0]
            if (data.status == 'login'){
                // Redirect the user to the login page
                window.location.href = data.redirect_url;
            }
            if (data.status == 'add') {
                $this.data('clicked', true);
                console.log('Clicked')
                product = `<div class="product product-cart">
                <figure class="product-media">
                <a href="/product-detail/${ref.id}/">
                    <img src="${data.data.product_img}" alt="product" width="80" height="88" />
                </a>
                <button class="btn btn-link btn-close remove_wishlist" pid="${ref.id}">
                    <i class="fas fa-times"></i><span class="sr-only">Close</span>
                </button>
                </figure>
                <div class="product-detail">
                <a href="/product-detail/${ref.id}/" class="product-name">${ref.title}</a>
                <div class="price-box">
                <span class="product-price">Rs.${ref.discounted_price}</span>
                </div>
                </div>
                
                </div>`
                product2 = `    
                <div class="products scrollable" id="main-wishlist">
                <div class="product product-cart">
                <figure class="product-media">
                <a href="/product-detail/${ref.id}/">
                    <img src="${data.data.product_img}" alt="product" width="80"
                    height="88" />
                </a>
                <button class="btn btn-link btn-close remove_wishlist" pid="${ref.id}">
                    <i class="fas fa-times"></i><span class="sr-only">Close</span>
                </button>
                </figure>
                <div class="product-detail">
                <a href="/product-detail/${ref.id}/" class="product-name">${ref.title}</a>
                <div class="price-box">
                <span class="product-price">Rs.${ref.discounted_price}</span>
                </div>
                </div>
                </div>
                </div>
                `
                    if (document.getElementById('main-wishlist') != null) {
                        console.log('if runs')
                        document.getElementById("main-wishlist").insertAdjacentHTML('afterbegin', product)
                    } else {
                        console.log('else runs')
                        console.log(document.querySelector('#wishlist').insertAdjacentHTML('afterend', product2))
                    }
                    if ((document.getElementById("no-wishlist")) != null) {
                        document.getElementById("no-wishlist").innerHTML = ''
                    }
                }
        }
    })
})

$(document).on('click', '.addtocart', function () {
    console.log('AddToCart Clicked')
    prod_id = $(this).attr('pid').toString()
    prod_qty = $('#product_qty') ? $('#product_qty').val() : '' 
    var variation_select = $('#variation-select').find(":selected").val() != undefined ? $('#variation-select').find(":selected").val() : 'None';
    console.log(variation_select , 'variation_select')
    console.log( prod_qty , 'prod qty')
    var $this = $(this); 
    $.ajax({
        type: "GET",
        url: "/add-to-cart/",
        data: { prod_id: prod_id , prod_qty : prod_qty , variation_select : variation_select },
        beforeSend: function () {
            $('.addtocart').attr('disabled', true);
        },
        success: function (data) {
            $('.addtocart').attr('disabled', false);
            console.log(data.status)
            if (data.status == 'login'){
                // Redirect the user to the login page
                window.location.href = data.redirect_url;
            }
            if (data.status == 'quantity error'){
                $('#product-error').html(`<div class="alert alert-light alert-danger alert-icon alert-inline mb-4">
				<i class="fas fa-exclamation-triangle"></i>
				<h4 class="alert-title">${data.error}</h4>
			</div>`)
            }
            if (data.status == 'add') {
                navcart = $('.cart-dropdown')
                navcart.addClass('opened')
                ref = data.data.product[0]
                $('.addtocart').attr('disabled', false);
                t = document.querySelectorAll('.Subtotal')
                t.forEach(element => {
                    element.innerText = `Rs: ${data.data.amount}`
                });
                c = document.querySelector('#count').innerText = data.data.count
                ides = document.querySelector('#item' + ref.id)
                // console.log(ides)
                if (($this.data('clicked') || !($this.data('clicked'))) && (ides != null)) {
                    // console.log(ides)
                    ides.innerText = data.data.quantity
                }
                else {
                    $this.data('clicked', true);
                    console.log('Clicked')
                    product = `<div class="product product-cart">
                <figure class="product-media">
                <a href="/product-detail/${ref.id}/">
                    <img src="${data.data.product_img}" alt="product" width="80"
                    height="88" />
                </a>
                <button class="btn btn-link btn-close remove_btn" pid="${ref.id}">
                    <i class="fas fa-times"></i><span class="sr-only">Close</span>
                </button>
                </figure>
                <div class="product-detail">
                <a href="/product-detail/${ref.id}/" class="product-name">${ref.title}</a>
                <div class="price-box">
                <span class="product-quantity" id="item${ref.id}" > ${data.data.quantity}</span>
                <span class="product-price">${ref.discounted_price}</span>
                </div>
                </div>
                
                </div>`
                product2 = `
                <div class="cart-header" id="cart-header">
                    <h4 class="cart-title">Shopping Cart</h4>
                    <a href="#" class="btn btn-dark btn-link btn-icon-right btn-close">close<i
                            class="d-icon-arrow-right"></i><span class="sr-only">Cart</span></a>
                </div>    
                <div class="products scrollable" id="nav-cart">
                <div class="product product-cart">
                <figure class="product-media">
                <a href="/product-detail/${ref.id}/">
                    <img src="${data.data.product_img}" alt="product" width="80"
                    height="88" />
                </a>
                <button class="btn btn-link btn-close remove_btn" pid="${ref.id}">
                    <i class="fas fa-times"></i><span class="sr-only">Close</span>
                </button>
                </figure>
                <div class="product-detail">
                <a href="/product-detail/${ref.id}/" class="product-name">${ref.title}</a>
                <div class="price-box">
                <span class="product-quantity" id="item${ref.id}" > ${data.data.quantity}</span>
                <span class="product-price">Rs.${ref.discounted_price}</span>
                </div>
                </div>
                </div>
                </div>
                <div class="cart-total">
                        <label>Subtotal:</label>
                        <span class="price Subtotal">Rs: ${data.data.amount}</span>
                </div>
                <div class="cart-action">
                    <a href="/cart/" class="btn btn-dark btn-link">View Cart</a>
                    <a href="/checkout/" class="btn btn-dark"><span>Go To
                            Checkout</span></a>
                </div>
                `
                    if (document.getElementById('nav-cart') != null) {
                        console.log('if runs')
                        document.getElementById("nav-cart").insertAdjacentHTML('afterbegin', product)
                    } else {
                        console.log('else runs')
                        $('#main-cart').html( product2 )
                    }
                    if ((document.getElementById("no-product")) != null) {
                        document.getElementById("no-product").innerHTML = ''
                    }
                }
            } else {
                
            }
        }
    })
})


$(document).on('click', ".remove_wishlist", function () {
    console.log("Remove Button Clicked")
    pid = $(this).attr("pid").toString()
    th = this
    $.ajax({
        type: "GET",
        url: "/delete_wishlist/",
        beforeSend: function () {
            $('.addtowishlist').attr('disabled', true);
            $('.addtowishlist i').append("<span class='loading'><span>");
            $('#cover-spin').show(0)
        },
        data: { prod_id: pid },
        success: function (data) {             
            var task = document.getElementsByClassName('remove_wishlist')
            $('.addtowishlist').attr('disabled', false);
            $('.addtowishlist i span').remove();
            $('#cover-spin').hide(0)
            for (let i = 0; i < task.length; i++) {
                if (task[i].getAttribute("pid") == pid) {
                    task[i].parentNode.parentNode.remove()
                }
            }
            th.parentNode.parentNode.remove()
            if (data.status == "Empty Cart") {
                console.log("Empty")
                main_cart = document.getElementById("wishlist")
                main_cart.innerHTML = ''
                main_cart.insertAdjacentHTML('afterend' , `<h4 class="heading mt-5 mb-5" id="no-product">No Product in Your Wishlist</h4>` )
            }
        }
    })
})


$(document).on('click', ".remove_btn", function () {
    console.log("Remove Button Clicked")
    pid = $(this).attr("pid").toString()
    th = this
    $.ajax({
        type: "GET",
        url: "/delete_cart/",
        beforeSend: function () {
            $('.addtocart').attr('disabled', true);
            $('.addtocart i').append("<span class='loading'><span>");
            $('#cover-spin').show(0)
        },
        data: { prod_id: pid },
        success: function (data) {             
            var task = document.getElementsByClassName('remove_btn')
            $('.addtocart').attr('disabled', false);
            $('.addtocart i span').remove();
            $('#cover-spin').hide(0)
            for (let i = 0; i < task.length; i++) {
                if (task[i].getAttribute("pid") == pid) {
                    task[i].parentNode.parentNode.remove()
                }
            }
            th.parentNode.parentNode.remove()
            c = document.querySelector('#count').innerText = data.data.count
            console.log(c)
            ides = document.querySelector('#item' + pid)
            document.querySelector('#count').innerText = data.data.count
            counpon_div = document.querySelector('.coupon_discount')
            if (counpon_div) {
                ccounpon_div.innerText = `- Rs ${data.data.coupon_discount}`
            }
            t = document.querySelectorAll('.Subtotal')
            t.forEach(element => {
                element.innerText = `Rs: ${data.data.amount}`
            });
            if (document.querySelector('.totalAmount')) {
                document.querySelector('.totalAmount').innerText = `Rs ${data.data.totalAmount}`
            }
            check_shipping = document.getElementById('shipping_amount')
            if (check_shipping) {
                check_shipping.innerText = data.data.shipping
            }
            if (data.status == "Empty Cart") {
                console.log("Empty")
                $("#main-cart").html('<h4 class="heading mt-5 mb-5" id="no-product">No Product in Your Cart</h4>')
                console.log('main khtm')
                console.log(window.location.href)
            }
        }
    })
})

$("#search").keyup(function () {
    $("#search").val().toString()
    suggestBox = $('.autocom-box')
    searchWrapper = document.querySelector('.search-input')
    searchInput = document.querySelector('.search-input input')
    $.ajax({
        url: '/search/',
        type: 'GET',
        data: { data: da },
        success: function (data) {
            x = data.data
            console.log(x)
            if (x.length > 0 & x != "n") {
                sug = ""
                for (i = 0; i < x.length; i++) {
                    sug += "<li onclick='search(this)' >" + data.data[i].title + "</li>";
                }
                document.querySelector(".autocom-box").innerHTML = sug
                searchWrapper.classList.add('active');

            } else {
                searchWrapper.classList.remove('active');
            }
        }
    })
})

function search(e) {
    text = e.innerText
    searchInput.value = text
    console.log(searchInput)

}

function myFun() {
    var x = document.getElementById("id_password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }

    if ($(".icon i").hasClass("fa-solid fa-eye-slash")) {
        $(".icon i").removeClass("fa-solid fa-eye-slash")
        $(".icon i").addClass("fa-solid fa-eye")
    } else {
        $(".icon i").removeClass("fa-solid fa-eye")
        $(".icon i").addClass("fa-solid fa-eye-slash")

    }
}



const searchInput = document.getElementById('search-input');
const searchSuggestions = document.getElementById('search-suggestions');

searchInput.addEventListener('input', () => {
    const query = searchInput.value;
    if (!query) {
        searchSuggestions.innerHTML = '';
        return;
    }

    // Send an AJAX request to the server
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/search?q=' + encodeURIComponent(query));
    xhr.onprogress = () => {
        $('.btn-search').html('<span class="loading-spinner" role="status" aria-hidden="true"></span>')
        
    };
    xhr.onload = () => {
        $('.btn-search span').remove()
        $('.btn-search').html('<i class="d-icon-search"></i>')
        if (xhr.status === 200) {
            var suggestions = JSON.parse(xhr.responseText);
            // Update the search suggestions
            searchSuggestions.innerHTML = suggestions.map(s => {
                const re = new RegExp(query, 'gi');
                const highlighted = s.title.replace(re, '<strong>$&</strong>');
                return `<div class="autocomplete-suggestion" data-index="1"><img class="search-image" src="${s.img}"><a href="${s.url}"><li>${highlighted}</li></a><span class="search-price">Rs ${s.price}</span></div>`;
            }).join('');

        }
    };
    xhr.send();
});
const searchInput_1 = document.getElementById('search-input-1');
const searchSuggestions_1 = document.getElementById('search-suggestions-1');

searchInput_1.addEventListener('input', () => {
    const query = searchInput_1.value;
    if (!query) {
        searchSuggestions_1.innerHTML = '';
        return;
    }

    // Send an AJAX request to the server
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/search?q=' + encodeURIComponent(query));
    xhr.onprogress = () => {
        $('.btn-search').html('<span class="loading-spinner" role="status" aria-hidden="true"></span>')
        
    };
    xhr.onload = () => {
        $('.btn-search span').remove()
        $('.btn-search').html('<i class="d-icon-search"></i>')
        if (xhr.status === 200) {
            const suggestions = JSON.parse(xhr.responseText);
            // Update the search suggestions
            searchSuggestions_1.innerHTML = suggestions.map(s => {
                const re = new RegExp(query, 'gi');
                const highlighted = s.title.replace(re, '<strong>$&</strong>');
                return `<div class="autocomplete-suggestion" data-index="1"><img class="search-image" src="${s.img}"><a href="${s.url}"><li>${highlighted}</li></a><span class="search-price">Rs ${s.price}</span></div>`;
            }).join('');

        }
    };
    xhr.send();
});


$(document).ready(function () {
    var $loading = $('.loading');
    $('#filter-form').submit(function (e) {
        e.preventDefault();
        $loading.addClass('is-active');
        var min_price = $('#min_price').val();
        var max_price = $('#max_price').val();
        $.ajax({
            url: '/filter-by-price/' + min_price + '/' + max_price + '/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $loading.removeClass('is-active');
                // update the HTML to show the filtered products
                $('.product-wrapper').html('');
                data.forEach(function (product) {
                    $('.product-wrapper').append(
                        `
                    <div class="product-wrap">
                    <div class="product">
                    <figure class="product-media">
                    <a href="/product-detail/${product.id}/">
                        <img src="${product.main_picture}" alt="product" width="280" height="315">
                    </a> ` + (product.discount_perc > 0 ? `<div class="product-label-group">
                    <label class="product-label label-sale">-${product.discount_perc}% off</label>
                </div>` : ``) + `
                    <div class="product-action-vertical">
                        <a href="#" class="btn-product-icon btn-cart addtocart" pid="${product.id}" data-toggle="modal"
                            data-target="#addCartModal" title="Add to cart"><i
                                class="d-icon-bag"></i></a>

                    </div>
                    <div class="product-action">
                        <a href="/product-detail/${product.id}/" class="btn-product"
                            title="Quick View">Quick View</a>
                    </div>
                </figure>
                <div class="product-details" style="max-width: 28rem;">
                    <div class="product-cat">
                        <a href="">${product.sub_categories}</a>
                    </div>
                    <h3 class="product-name">
                        <a href="">${product.title}</a>
                    </h3>
                    <div class="product-price">
                        <ins class="new-price">Rs: ${product.discounted_price}</ins><del
                            class="old-price">Rs: ${product.selling_price}</del>
                    </div>
                    ` + (reviews > 0 ? `
                    <div class="ratings-container">
                        <div class="ratings-full">
                            <span class="ratings" style="width:${rating}%"></span>
                            <span class="tooltiptext tooltip-top"></span>
                        </div>
                        <a href="/product-detail'/${product.id}/" class="rating-reviews">( ${product.reviews} reviews
                            )</a>
                    </div>
                    ` : '') + `
                    
                    </div>
                </div>
                </div>
                </div>
            </div>
        </div>`
                    );
                });
            }
        });
    });
});
var passwordform = false
$("#password_change_form").submit(function (e) {
    passwordform = true
    e.preventDefault();
    var form = $(this);
    var passwordbtn = $('.passwordbtn')
    var url = form.attr("action");
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        dataType: "json",
        beforeSend: function () {
            passwordbtn.attr('disabled', true)
            passwordbtn.html('<span class="loading-spinner" role="status" aria-hidden="true"></span> Loading...');
        },
        success: function (data) {
            if (passwordform) {
                $('span[id$="_err"]').text('');
                passwordform = false;
            }
            $('.passwordbtn span').remove()
            passwordbtn.attr('disabled', false)
            $('.passwordbtn').html('Change Password');
            if (data.status == 'success') {
                document.getElementById('change_password_success').innerText = 'Passoword Changed Successfully!!! '
            } else {
                // Show error messages
                for (var error in data.errors) {
                    console.log(error)
                    $("#" + error + "_err").text(data.errors[error]);
                }
            }
        }
    });
});

var RegisterForm = false;
$("#user_creation_form").submit(function (e) {
    var RegisterForm = true
    e.preventDefault();
    var form = $(this);
    var registerbtn = $('.register-btn')
    var url = form.attr("action");
    $.ajax({
        type: "POST",
        url: url,
        beforeSend: function () {
            registerbtn.attr('disabled', true)
            registerbtn.html('<span class="loading-spinner" role="status" aria-hidden="true"></span> Loading...');
        },
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
            if (RegisterForm) {
                $('small[id$="_error"]').text('');
                RegisterForm = false;
            }
            $('.register-btn span').remove()
            registerbtn.attr('disabled', false)
            $('.register-btn').html('Register');
            if (data.status == 'success') {
                // Show success message
                window.location.href = data.redirect_url;
            } else {
                // Show error messages
                for (var error in data.errors) {
                    $("#" + error + "_error").text(data.errors[error]);
                }
            }
        }
    });
});
var LoginFormSubmitted = false;
$("#user_login_form").submit(function (e) {
    LoginFormSubmitted = true;
    e.preventDefault();
    var form = $(this);
    var loading_element = $('.login-btn')
    var url = form.attr("action");
    $.ajax({
        beforeSend: function () {
            loading_element.attr('disabled', true)
            loading_element.html('<span class="loading-spinner" role="status" aria-hidden="true"></span> Loading...');
        },
        type: "POST",
        url: url,
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
            if (LoginFormSubmitted) {
                $('small[id$="_errors"]').text('');
                LoginFormSubmitted = false;
            }
            $('.login-btn span').remove()
            loading_element.attr('disabled', false)
            $('.login-btn').html('Login');
            if (data.status == 'success') {
                window.location.href = data.redirect_url;
            }
            if (data.status == 'error') {
                // Show success message
                for (var error in data.errors) {
                    console.log(error)
                    $("#" + error + "_errors").text(data.errors[error]);
                }
            }
        }
    });
});

$(document).ready(function() {
    $('#variation-select').change(function(){
        var variation_option = $(this).val().toString();
        var variation_select = document.querySelector('#variation-select');
        var variation_value = variation_select.options[variation_select.selectedIndex].getAttribute('value').toString();
        var product_id = variation_select.options[variation_select.selectedIndex].getAttribute('pid').toString();
        var price = variation_select.options[variation_select.selectedIndex].getAttribute('price').toString();
        console.log(variation_value , 'variation value')
        console.log( product_id , 'product_id')
        console.log( price , 'price')
        $(".product-variation-price").children("p").html(`Rs ${price}`)


    })
})

$(document).ready(function () {
    $('#filter-select').change(function () {
        var option = $(this).val().toString();
        var select = document.querySelector("#filter-select");
        var category = select.options[select.selectedIndex].getAttribute('category').toString();
        var subcategory = select.options[select.selectedIndex].getAttribute('subcategory').toString();
        var subsubcategory = select.options[select.selectedIndex].getAttribute('subsubcategory').toString();
        $.ajax({
            url: '/filter-products/' + option + '/' + category + '/' + subcategory + '/' + subsubcategory + '/',
            type: 'GET',
            dataType: 'json',
            beforeSend: function () {
                $('#cover-spin').show(0)
            },
            success: function (data) {
                $('#cover-spin').hide(0)
                $('html, body').animate({ scrollTop: 0 }, 0);
                $('.product-wrapper').html('');
                $('#paginator').html('');
                data.forEach(function (product) {
                    $('.product-wrapper').append(`
                    <div class="product-wrap">
                        <div class="product product-image-gap text-center  cart-full">
                            <figure class="product-media">
                                <div class="product-img">
                                    <div onclick="window.location.href='${ product.get_absolute_url }'" style="cursor:pointer;">
                                        <img class="front-img" src="${product.main_picture}" alt="Best Seller" width="280"
                                            height="315" style="background-color: #f2f3f5;" />
                                            ` + ( product.hover_image ? `
                                        <img class="rear-img" src="${product.hover_image}" alt="Best Seller" width="280"
                                            height="315" style="background-color: #f2f3f5;" onmouseover="this.src='${product.hover_image}'"
                                            onmouseout="this.src='${product.hover_image}'" />
                                            ` : '' ) + `
                                    </div>
                                </div>
                                ` +
                                    (product.discount_perc > 0 ? ` 
                                <div class="product-label-group">
                                    <label class="product-label label-sale">-${product.discount_perc}% off</label>
                                </div>
                                ` : '') + ( (product.out_of_stock ) ? 
                                `<div class="OOS">Out of stock</div>` : '' ) + `

                                <div class="product-action-vertical"> 
                                <a href="#" class="btn-product-icon btn-wishlist addtowishlist"
                                pid="${product.id}" title="Add to wishlist"><i class="d-icon-heart"></i></a>
                                </div>
                            </figure>
                            <div class="product-details">
                                <div class="product-cat">
                                    <a href="/brand/${product.brand_url}">${product.brand}</a>
                                </div>
                                <h3 class="product-name">
                                    <a href="${product.get_absolute_url}">${product.title}</a>
                                </h3>
                                <div class="product-price">
                                    <span class="price">Rs.${product.discounted_price}</span>
                                    ` + ( product.selling_price ? `
                                        <del class="old-price">Rs.${product.selling_price}</del>
                                    ` : '' ) + ` 
                                </div>
                                ` + (product.reviews > 0 ? `
                                <div class="ratings-container">
                                    <div class="ratings-full">
                                        <span class="ratings" style="width:${product.rating}%"></span>
                                        <span class="tooltiptext tooltip-top"></span>
                                    </div>
                                    <a href="/product-detail/${product.id}/" class="rating-reviews">( ${product.reviews} reviews
                                        )</a>
                                </div>
                                ` : '') + ( !product.out_of_stock ?  ( product.type != '2' ? 
                                `<a class="btn-product-no-modal btn-cart addtocart"  pid="${product.id}" title="Add to cart"><i
                                class="d-icon-bag"></i>Add to cart</a>` :
                                 `<a class="btn-product-no-modal btn-cart" href="${ product.get_absolute_url }" title="Select Option"><i
                                class="d-icon-bag"></i>Select Option</a>`  ) : '' ) + `
                            </div>
                        </div>
                    </div>`
                    );
                });
            }
        });
    });
});


let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = document.getElementById("slider-1");

function slideOne() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    displayValOne.textContent = `Rs ${sliderOne.value}`;
    fillColor();
}
function slideTwo() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    displayValTwo.textContent = `Rs ${sliderTwo.value}`;
    fillColor();
}
function fillColor() {
    percent1 = (sliderOne.value / sliderMaxValue) * 100;
    percent2 = (sliderTwo.value / sliderMaxValue) * 100;
    sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #444 ${percent1}% , #444 ${percent2}%, #dadae5 ${percent2}%)`;
}

$("#filter_by_price").submit(function (e) {
    e.preventDefault();
    category = $("input[name=data]").attr("category").toString();
    subcategory = $("input[name=data]").attr("subcategory").toString();
    subsubcategory = $("input[name=data]").attr("subsubcategory").toString();
    console.log($(this).val())
    min_price = $("#slider-1").val().toString();
    max_price = $("#slider-2").val().toString();
    loading_element = $("#filterbtn")
    console.log(min_price)
    console.log(max_price)
    $.ajax({
        url: '/filter-by-price/' + min_price + '/' + max_price + '/',
        type: 'GET',
        data: { 'category': category, 'subcategory': subcategory , 'subsubcategory': subsubcategory },
        dataType: 'json',
        beforeSend: function () {
            loading_element.attr('disabled', true)
            loading_element.html('<span class="loading-spinner" role="status" aria-hidden="true"></span> Loading...');
        },
        success: function (data) {
            $('.btn-filter span').remove()
            loading_element.html('Filter')
            loading_element.attr('disabled', false)
            $('.product-wrapper').html('');
            $('#paginator').html('');
            data.forEach(function (product) {
                $('.product-wrapper').append(`
                    <div class="product-wrap">
                        <div class="product product-image-gap text-center cart-full"  style="height: 384px;" >
                            <figure class="product-media">
                                <div class="product-img">
                                    <div onclick="window.location.href='${ product.get_absolute_url }'" style="cursor:pointer;">
                                        <img class="front-img" src="${product.main_picture}" alt="${product.title}" width="280"
                                            height="315" style="background-color: #f2f3f5;  height: 220px; " />
                                            ` + ( product.hover_image ? `
                                        <img class="rear-img" src="${product.hover_image}" alt="${product.title}" width="280"
                                            height="315" style="background-color: #f2f3f5;  height: 220px;  " onmouseover="this.src='${product.hover_image}'"
                                            onmouseout="this.src='${product.hover_image}'" />
                                            ` : '' ) + `
                                    </div>
                                </div>
                                ` +
                                    (product.discount_perc > 0 ? ` 
                                <div class="product-label-group">
                                    <label class="product-label label-sale">-${product.discount_perc}% off</label>
                                </div>
                                ` : '') + ( (product.out_of_stock ) ? 
                                `<div class="OOS">Out of stock</div>` : '' ) + `

                                <div class="product-action-vertical"> 
                                <a href="#" class="btn-product-icon btn-wishlist addtowishlist"
                                pid="${product.id}" title="Add to wishlist"><i class="d-icon-heart"></i></a>
                                </div>
                            </figure>
                            <div class="product-details">
                                <div class="product-cat">
                                    <a href="/brand/${product.brand_url}">${product.brand}</a>
                                </div>
                                <h3 class="product-name">
                                    <a href="${product.get_absolute_url}">${product.title}</a>
                                </h3>
                                <div class="product-price">
                                    <span class="price">Rs.${product.discounted_price}</span>
                                    ` + ( product.selling_price ? `
                                        <del class="old-price">Rs.${product.selling_price}</del>
                                    ` : '' ) + ` 
                                </div>
                                ` + (product.reviews > 0 ? `
                                <div class="ratings-container">
                                    <div class="ratings-full">
                                        <span class="ratings" style="width:${product.rating}%"></span>
                                        <span class="tooltiptext tooltip-top"></span>
                                    </div>
                                    <a href="/product-detail/${product.id}/" class="rating-reviews">( ${product.reviews} reviews
                                        )</a>
                                </div>
                                ` : '') + ( !product.out_of_stock ?  ( product.type != '2' ? 
                                `<a class="btn-product-no-modal btn-cart addtocart"  pid="${product.id}" title="Add to cart"><i
                                class="d-icon-bag"></i>Add to cart</a>` :
                                 `<a class="btn-product-no-modal btn-cart" href="${ product.get_absolute_url }" title="Select Option"><i
                                class="d-icon-bag"></i>Select Option</a>`  ) : '' ) + `
                            </div>
                        </div>
                    </div>`
                );
            });
        }
    });
});


$('#btn-order').submit(function (e) {
    e.preventDefault();
    console.log($(this))
    $(this).attr('disabled', true)
    $(this).html('<span class="loading-spinner" role="status" aria-hidden="true"></span> Loading...');
})

document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.payment.accordion.radio-type a');
    const paymentMethodInput = document.getElementById('payment-method-input');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            console.log(event.target.innerText)
            console.log(event.target)
            paymentMethodInput.value = event.target.innerText
        });
    });
});

$(document).ready(function () {
    $('.payment.accordion.radio-type a').click(function (event) {
        event.preventDefault(); // Prevent default link behavior

        var paymentMethod = $(this).text().trim();
        //   console.log(paymentMethod)

        // Make an AJAX call to update the total based on the selected payment method
        $.ajax({
            url: '/update_total/',
            type: 'GET',
            data: { paymentMethod: paymentMethod },
            dataType: "json",
            beforeSend: function () {
                $('#cover-spin').show(0)
            },
            success: function (data) {
                $('#cover-spin').hide(0)
                discount_div = `<tr class="summary-shipping">
            <td>
            <h4 class="summary-subtitle">Fix Discount</h4>
            </td>
            <td class="summary-subtotal-price pb-0 pt-0 c-discount">Rs ${data.fix_discount}
            </td>
            </tr>`
                // Update the total element with the new value returned from the server
                if (data.fix_discount && document.querySelector('.summary-shipping') == null) {
                    document.querySelector('.summary-total').insertAdjacentHTML('beforebegin', discount_div)
                } else {
                    $('.c-discount').innerText = `Rs ${data.fix_discount}`
                }
                if (paymentMethod == 'Cash On Delivery') {
                    // console.log("Cash on delivery2")
                    if (document.querySelector('.summary-shipping') != null) {
                        $('.summary-shipping').remove()
                    }
                }
                document.getElementById('c-amount').innerText = `Rs ${data.amount}`
                document.getElementById('c-total').innerText = `Rs ${data.totalAmount}`

                //   $('#total').text(data);
            },

        });
    });
});


$(document).ready(function() {
    var hash = window.location.hash; // Get the hash from the URL
    if (hash === '#orders') { // Check if the hash matches the target tab
        $('#dashboard-tab-link').removeClass('active'); // Add "active" class to the tab link
        $('#dashboard').removeClass('active show'); // Add "active" and "show" classes to the tab content
        $('#orders-tab-link').addClass('active'); // Add "active" class to the tab link
        $('#orders').addClass('active show'); // Add "active" and "show" classes to the tab content
        console.log('han han he')
    }
  });
  
$(document).ready(function () {
    $('.popup-view').click(function (event) {
        console.log('click');
        product_id = $(this).attr("pid").toString();
        console.log(product_id)
        $.ajax({
            url: "/quick-view/",
            type: "GET",
            data: { prod_id: product_id },
            beforeSend: function () {
            },
            success: function (data) {
                $('#product-modal').show();

            }
        })
    })
});

$('#product-modal .close').click(function () {
    $('#product-modal').hide();
});


// For Flash Sale
var check = document.getElementById('remaining-time');
if (check) {
    var remainingT = document.getElementById('remaining-time').textContent;
    console.log(remainingT)

    const durationStr = remainingT;
    const durationRegex = /(\d+)DT(\d+)H(\d+)M(\d+\.\d+)S/;
    const durationMatch = durationStr.match(durationRegex);
    var days = parseInt(durationMatch[1])
    const hours = parseInt(durationMatch[2]);
    const minutes = parseInt(durationMatch[3]);
    const seconds = parseFloat(durationMatch[4]);
    var remainingTime = (hours * 60 * 60) + (minutes * 60) + seconds;

    var timer = setInterval(function () {
        remainingTime--;
        if (remainingTime <= 0) {
            clearInterval(timer);
            location.reload();  // reload the page to update the product price
        }
        var hours = Math.floor(remainingTime / (60 * 60));
        var minutes = Math.floor((remainingTime % (60 * 60)) / 60);
        var seconds = Math.floor(remainingTime % 60);
        if (days) {
            var timerStr = days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's';
        } else {
            var timerStr = hours + 'h ' + minutes + 'm ' + seconds + 's';
        }
        document.querySelector('#flash-sale-timer').textContent = timerStr;
    }, 1000);
}

$(document).ready(function () {
    // Get the width of the container
    var containerWidth = $("#fitin").width();

    // Get the width of the content
    var contentWidth = $("#fitin").children().width();

    // Check if the content is wider than the container
    if (contentWidth > containerWidth) {
        // If it is, compress the font size to fit
        var fontSize = parseInt($("#fitin").children().css("font-size"));
        while (contentWidth > containerWidth) {
            fontSize--;
            $("#fitin").children().css("font-size", fontSize + "px");
            contentWidth = $("#fitin").children().width();
        }
    }
});


function openModal() {
    document.getElementById("myModal").style.display = "block";
  }
  
function closeModal() {
document.getElementById("myModal").style.display = "none";
}

var CouponForm = false;
$("#coupon-form").submit(function (e) {
    CouponForm = true;
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");
    loading_element = $('#coupon-btn')
    cart_id = $('#cart_id');
    coupon_code = $("#coupon_code").val()
    console.log(coupon_code)
    $.ajax({
        beforeSend: function () {
            loading_element.attr('disabled', true)
            loading_element.html('<span class="loading-spinner" role="status" aria-hidden="true"></span> Loading...');
        },
        type: "POST",
        url: url,
        data : form.serialize(),
        dataType: "json",
        success: function (data) {
            $('.coupon-btn span').remove()
            loading_element.attr('disabled', false)
            $('#coupon-btn').html('Apply Coupon');
            console.log(data)

            if (data.status == 'not-exist') {
                $("#for-coupon-error").html(`<div class="alert alert-light alert-danger alert-icon alert-inline mb-4" style="max-width: 500px;">
                <i class="fas fa-exclamation-triangle"></i>
                The coupon code <span class="highlight-placeholder">${coupon_code}</span> is not valid.
                </div>`)
            }
            else if (data.status == 'already-exist') {
                $("#for-coupon-error").html(`<div class="alert alert-light alert-danger alert-icon alert-inline mb-4" style="max-width: 500px;">
                <i class="fas fa-exclamation-triangle"></i>
                The coupon code <span class="highlight-placeholder">${coupon_code}</span> coupon code already applied.
                </div>`)
            }
            else if (data.status == 'success') {
                data = data.data
                console.log(data.cart_discount)
                $("#for-coupon-error").html(`<div class="alert alert-simple alert-primary alert-icon mb-4">
                <i class="fas fa-check"></i>
                Coupon Discount Rs.${data.coupon_discount} Added Successfully !!!
                </div>`)
            document.querySelector('.totalAmount').innerText = `Rs ${data.totalAmount}`
            t = document.querySelectorAll('.Subtotal')
            t.forEach(element => {
                element.innerText = `Rs: ${data.amount}`
            });
            $('#cart-table').prepend($(`<tr class="summary-subtotal">
            <td>
                <h4 class="summary-subtitle">Coupon Discount</h4>
            </td>
            <td>
                <p class="summary-subtotal-price Subtotal">Rs.${data.coupon_discount}</p>
            </td>												
            </tr>`));
            }
        }
    })
})

$(document).ready(function() {
    var cityField = $('#id_city');
    var otherOption = 'Other';

    cityField.change(function() {
        console.log("City function run ")
        if (cityField.val() === otherOption) {
            cityField.replaceWith('<input type="text" id="id_city" name="city" class="form-control" maxlength="200" required placeholder="Enter Your City Name" >');
        }
    });
});
