(function() {
    var app = angular.module("timeslots", ['ui.bootstrap']);
    
    app.controller('TimeslotCtrl', ['$scope', function($scope) {
        
        $scope.country = 'china';

        $scope.cities = [["Peking","peking"], ["Shanghai","shanghai"], ["Guangzhou","guanzhou"], ["Chongqing","chongqing"]];
        $scope.city = $scope.cities[0];
        $scope.date = Date.now();
        $scope.time = undefined;        
        
    }]);
})();