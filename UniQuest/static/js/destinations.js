/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Menu
4. Init Input
5. Init Isotope


******************************/

$(document).ready(function()
{
	"use strict";

	/* 

	1. Vars and Inits

	*/

	var header = $('.header');
	var headerSocial = $('.header_social');
	var menu = $('.menu');
	var menuActive = false;
	var burger = $('.hamburger');

	setHeader();

	$(window).on('resize', function()
	{
		setHeader();

		setTimeout(function()
		{
			$(window).trigger('resize.px.parallax');
		}, 375);
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	initMenu();
	initInput();
	initIsotope();

	/* 

	2. Set Header

	*/

	function setHeader()
	{
		if($(window).scrollTop() > 127)
		{
			header.addClass('scrolled');
			headerSocial.addClass('scrolled');
		}
		else
		{
			header.removeClass('scrolled');
			headerSocial.removeClass('scrolled');
		}
	}

	/* 

	3. Set Menu

	*/

	function initMenu()
	{
		if($('.menu').length)
		{
			var menu = $('.menu');
			if($('.hamburger').length)
			{
				burger.on('click', function()
				{
					if(menuActive)
					{
						closeMenu();
					}
					else
					{
						openMenu();
					}
				});
			}
		}
		if($('.menu_close').length)
		{
			var close = $('.menu_close');
			close.on('click', function()
			{
				if(menuActive)
				{
					closeMenu();
				}
			});
		}
	}

	function openMenu()
	{
		menu.addClass('active');
		menuActive = true;
	}

	function closeMenu()
	{
		menu.removeClass('active');
		menuActive = false;
	}

	/* 

	4. Init Input

	*/

	function initInput()
	{
		if($('.newsletter_input').length)
		{
			var inpt = $('.newsletter_input');
			inpt.each(function()
			{
				var ele = $(this);
				var border = ele.next();

				ele.focus(function()
				{
					border.css({'visibility': "visible", 'opacity': "1"});
				});
				ele.blur(function()
				{
					border.css({'visibility': "hidden", 'opacity': "0"});
				});

				ele.on("mouseenter", function()
				{
					border.css({'visibility': "visible", 'opacity': "1"});
				});

				ele.on("mouseleave", function()
				{
					if(!ele.is(":focus"))
					{
						border.css({'visibility': "hidden", 'opacity': "0"});
					}
				});
				
			});
		}
	}

	/* 

	5. Init Isotope

	*/

	function initIsotope()
{
    // Enable isotope on all devices including mobile
    if($('.item_grid').length)
    {
        var grid = $('.item_grid').isotope({
            itemSelector: '.item',
            layoutMode: 'fitRows', // Change to fitRows for better grid behavior
            getSortData:
            {
                price: function(itemElement)
                {
                    var priceEle = $(itemElement).find('.destination_price').text().replace( 'From $', '' );
                    return parseFloat(priceEle);
                },
                name: '.destination_title a'
            },
            animationOptions:
            {
                duration: 750,
                easing: 'linear',
                queue: false
            }
        });

        // Refresh isotope on window resize to handle responsive changes
        $(window).on('resize', function() {
            setTimeout(function() {
                grid.isotope('layout');
            }, 300);
        });

        // Sort based on the value from the sorting_type dropdown
        sortingButtons.each(function()
        {
            $(this).on('click', function()
            {
                var parent = $(this).parent().parent().find('.sorting_text');
                parent.text($(this).text());
                var option = $(this).attr('data-isotope-option');
                option = JSON.parse( option );
                grid.isotope( option );
            });
        });
    }
}



});