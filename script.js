function get_airports() {
	$(".loading").show();
	$.ajax({
		type: "GET",
		url: "http://flowmaster.org:8888/airports/",
		//data: { param: input },
		success: callback_get_airports
		});
}
function show_initial(source, destination){
	$(".main").html(function(){
		source = "<div class='state initial_state'>"+source+"</div>";
		intermediate = "<div class='intermidiate'><div class='loading1'></div></div>"
		destination = "<div class='state initial_state'>"+destination+"</div>";
		return source + intermediate + destination
	});
}

function callback_get_airports(response) {
	// do something with the response
	var data = response["data"]
	var status = response["status"]
	var options = {
		data: data,
		getValue: "name",
		list: {
			match: {
				enabled: true
			}
		}

	};
	$(".loading").hide();
	$("body").removeAttr("style");
	$("#header").removeClass("load");
	$("#src").easyAutocomplete(options);
	$("#destination").easyAutocomplete(options);
}

function find_optimal_routes(){

	var source = $("#src").val();
	var destination = $("#destination").val();

	source = source.split(' - ');
	destination = destination.split(' - ');
	show_initial(source[0], destination[0]);
	request = "http://flowmaster.org:8888/optimal/"+source[source.length-1]+"/"+destination[destination.length-1]+"/";
	$(".loading1").show();
	$.ajax({
		type: "GET",
		url: request,
		success: callback_return_optimal
	});
}

function callback_return_optimal(response){
	$(".loading1").hide();
	console.log(response);
	if (response["found"] == "No"){
		$(".main").append("No flights found between these cities<br><a href='.'>Try again</a></div>");
		return
	}
	var direct = response["direct"];
	var routes = response["routes"];
	var num = response["flightNum"];
	var optimal = response.optimal;
	var isDirect = isIn(optimal, routes);

	if (isDirect == false){
		if(direct){
			$(".intermidiate").append("<div class='best state'>"+direct+"</div>");
		}
		for (route in routes){
			$(".intermidiate").append("<div class='state'>" +routes[route]["first"]+" "+routes[route]["name"]+" "+routes[route]["second"]+"</div>");
		}
	}else{
		if(direct){
			$(".intermidiate").append("<div class='state'>"+direct+"</div>");
		}
		for (route in routes){
			if (routes[route]["name"] == optimal){
				state = "'best state'";
			}else{
				state = "'state'";
			}
			$(".intermidiate").append("<div class="+state+">" +routes[route]["first"]+" "+routes[route]["name"]+" "+routes[route]["second"]+"</div>");
		}
	}
	$(".main").prepend("<div>Total number of flights analyzed: "+ num+"</div>");
	$(".main").append("<div class='result'>The best route is: "+optimal+"</div><br><a href='.'>Try again</a></div>");
}

function isIn(needle, haystack){
	var length = haystack.length;
	for (var i = 0 ; i < length ; ++i){
		if (haystack[i]["name"] == needle) {
			return true;
		}
	}
	return false;
}

$(".find").click(function(){
	find_optimal_routes();
});
get_airports();
