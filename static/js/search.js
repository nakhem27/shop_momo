$(document).ready(function()
{
    var products = [
    "Handbags",
    "Bags",
    "Purse",
    "Wallets",
    "Wallet",
    "Cardcase",
    "Rexy",
    "Black",
    "Rogue",
    "Rogue 25",
    "Rexy Highline Tote",
    "Highline",
    "Tote",
    "Harmony Hobo",
    "Harmony",
    "Hobo",
    "Rexy Skeleton",
    "Skeleton",
    "Rexy Oil Slick",
    "Oilslick",
    "Rexy Gold",
    "Gold",
    "Foldover Card Case",
    "Foldover",
    "Rexy Card Holder",
    "Cardholder",
    "Rexy Zippy Wallet",
    "Zippy",
    "Zippy wallet"
    ];

    $('#form-autocomplete').autocomplete({
        source: products
    });

    $('#form-autocomplete2').autocomplete({
        source: products
    });

});