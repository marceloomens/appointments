(function() {
    var app = angular.module("timeslots", ['ui.bootstrap']);
    
    app.controller('TimeslotCtrl', ['$scope', '$http', '$log', function($scope, $http, $log) {

        $scope.countryChanged = function() {
            $scope.clearCity();
            if (null === $scope.country) {
            } else {
                $http.get('/api/locations/'+$scope.country.fields.slug, {cache: true}).
                    success(function(data, status, headers, config) {
                        $scope.cities = data;
                    }).
                    error(function(data, status, headers, config) { 
                    });  
            }
        }
        
        $scope.clearCountry = function() {
            $scope.countries = []
            $scope.country = null;            
            $scope.clearCity();
        }

        $scope.cityChanged = function() {
            $scope.clearDate();
            if (null === $scope.city) {   
            } else {
                $http.get('/api/timeslots/'+$scope.city.fields.slug, {cache: true}).
                    success(function(data, status, headers, config) {
                        $scope.datetimes = data;
                        $scope.mindate = new Date(data.minbound);
                        var maxdate = new Date(data.maxbound);
                        // Set date is hardened for edge cases (i.e. 0, -1, 32...)
                        maxdate.setDate(maxdate.getDate()-1);
                        $scope.maxdate = maxdate;
                    }).
                    error(function(data, status, headers, config) {
                    });
            }
        }
        
        $scope.clearCity = function() {
            $scope.cities = [];
            $scope.city = null;
            $scope.clearDate();    
        }

        $scope.dateChanged = function() {
            $scope.clearTime();
            if (null === $scope.date) {
            } else {
                key = $scope.keyForDate($scope.date)
                $scope.timeslots = $scope.datetimes.data[key].timeslots.sort();
            }
        }

        $scope.clearDate = function() {
            $scope.datetimes = null;
            $scope.mindate = null;
            $scope.maxdate = null;
            $scope.date = null;
            $scope.clearTime();
        }
            
        $scope.clearTime = function() {
            $scope.timeslots = [];
            $scope.time = null;            
        }
        
        $scope.disabled = function(date, mode) {
    
            if ($scope.datetimes === null) return true;
            key = $scope.keyForDate(date);
            if ($scope.datetimes.data[key] === undefined) return true;
            return !($scope.datetimes.data[key].code === 0);
        }
        
        $scope.keyForDate = function(date) {
            var d = date.getDate(), m = date.getMonth()+1, y = date.getFullYear();
            d = d < 10 ? "0" + d : d;
            m = m < 10 ? "0" + m : m;
            return (y + "-" + m + "-" + d);
        }
        
        $scope.clearCountry();

        $http.get('/api/countries/', {cache: true}).
            success(function(data, status, headers, config) {
                $scope.countries = data;
            }).
            error(function(data, status, headers, config) { 
            });
        
    }]);
})();