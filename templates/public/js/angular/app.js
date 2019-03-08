/**
 * Created by erlan on 9/1/17.
 */

var app = angular.module('MyBrands', ['ngCookies']);

app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
}]);

app.filter('search', function () {
    return function (obj, searchWord) {
        if (searchWord === '' || searchWord === undefined || searchWord === null) return obj;

        var xRegex = '';
        if (searchWord.indexOf(' ') > -1) {
            var words = searchWord.split(' ');
            for (var i = 0; i < words.length; ++i) {
                xRegex += words[i].toLowerCase() + ' ';
            }
        } else {
            xRegex += searchWord.toLowerCase();
        }
        xRegex = new RegExp(xRegex, 'i');
        var resultToReturn = [];
        for (var i = 0; i < obj.length; ++i) {
            console.log(obj[i].title.toLowerCase(), xRegex);
            if (obj[i].title.toLowerCase().match(xRegex) !== null) {
                resultToReturn.push(obj[i]);
            }
        }
        return resultToReturn;
    }
});

app.filter('calculate_discount', function () {
    return function (price, discount) {
        return price - ((price * discount) / 100);
    }
});

app.controller('FilterController',
    [
        '$scope', '$http', '$cookies',
        function ($scope, $http, $cookies) {
            $scope.controllerData = {};
            $http({
                url: GET_PRODUCT_URL,
                method: 'POST',
                data: {'csrfmiddlewaretoken': $cookies.get('csrftoken')},
                headers: {'Content-Type': 'application/json'}
            }).then(function (response) {
                products = [];
                for (var item in response.data.data) {
                    if (response.data.data.hasOwnProperty(item)) {
                        products.push(response.data.data[item]);
                    }
                }
                $scope.controllerData.products = products;
            }, function (error) {
                console.error(error);
            });

            $scope.applyFilters = function () {
                var data = {
                    'min_price': $scope.controllerData.minPrice,
                    'max_price': $scope.controllerData.maxPrice,
                    'csrfmiddlewaretoken': $cookies.get('csrftoken')
                };

                $.ajax({
                    url: GET_PRODUCT_URL,
                    method: 'POST',
                    data: data,
                    dataType: 'JSON',
                    success: function (response) {
                        $scope.controllerData.products = response.data;
                        $scope.$apply();
                    }
                });
            };
        }
    ]
);
