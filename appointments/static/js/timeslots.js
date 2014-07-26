(function() {
    var app = angular.module("timeslots", ['ui.bootstrap']);
    
    app.config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }]);
    
    app.controller('TimeslotCtrl', ['$scope', '$http', '$window', '$log', function($scope, $http, $window, $log) {

        // Country
        $scope.clearCountry = function() {
            $scope.countries = [];
            $scope.country = undefined;            
            $scope.clearCity();
        };
        
        $scope.countryChanged = function() {
            $scope.clearCity();
            if (undefined === $scope.country) {
            } else {
                $http.get('/api/locations/'+$scope.country, {cache: true}).
                    success(function(data, status, headers, config) {
                        $scope.cities = data;
                    }).
                    error(function(data, status, headers, config) { 
                    });  
            }
        }

        // City
        $scope.clearCity = function() {
            $scope.cities = [];
            $scope.appointment.constraint = undefined;
            $scope.clearDate();
            $scope.clearAction();
        }

        $scope.cityChanged = function() {
            $scope.clearDate();
            if (undefined === $scope.appointment.constraint) {   
            } else {
                // Obtain actions for city
                $http.get('/api/actions/'+$scope.appointment.constraint, {cache: true}).
                    success(function(data, status, headers, config) {
                        $scope.actions = data;
                    }).
                    error(function(data, status, headers, config) {
                    });
                // Obtain timeslots for city
                $http.get('/api/timeslots/'+$scope.appointment.constraint, {cache: true}).
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

        // Date
        $scope.clearDate = function() {
            // I need a naive date; js Date isn't; I'll convert it naively upon form submission.
            $scope.date = undefined;
            $scope.datetimes = null;
            $scope.mindate = undefined;
            $scope.maxdate = undefined;
            $scope.clearTime();
        }
            

        $scope.dateChanged = function() {
            $scope.clearTime();
            if (undefined === $scope.date) {
            } else {
                key = $scope.keyForDate($scope.date)
                $scope.timeslots = $scope.datetimes.data[key].timeslots.sort();
            }
        }

        // Time
        $scope.clearTime = function() {
            $scope.timeslots = [];
            $scope.appointment.time = undefined;            
        }
        
        // Action        
        $scope.clearAction = function() {
            $scope.actions = [];
            $scope.appointment.action = undefined;
        }

        // Datepicker  
        $scope.disabled = function(date) {            
    
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
        
        // Init
        $scope.country = undefined;
        
        $scope.appointment = {
            constraint : undefined,
            date : undefined,
            time : undefined,
            action : undefined
        }
        
        $scope.clearCountry();

        $http.get('/api/countries/', {cache: true}).
            success(function(data, status, headers, config) {
                $scope.countries = data;
            }).
            error(function(data, status, headers, config) { 
        });
        
        // Submit
        $scope.submit = function() {
            // Convert my Date object naively...
            $scope.appointment.date = $scope.keyForDate($scope.date);
            // $log.log($scope.appointment);
            $http.post('/book/', $scope.appointment).
                success(function(data, status, headers, config) {
                    $window.location.href = '/finish/';
                }).
                error(function(data, status, headers, config) {
                });
        }

    }]);
})();