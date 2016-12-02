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
	var direct = response["direct"]
	if(direct){
		$(".intermidiate").append("<div class='state'>"+direct+"</div>")
	}
	var routes = response["routes"]
	for (route in routes){
		$(".intermidiate").append("<div class='state'>" +routes[route]["first"]+" "+routes[route]["name"]+" "+routes[route]["second"]+"</div>");
	}
	var optimal = response.optimal
	$(".main").append("<div >The best route " + optimal+ "</div>");
}

$(".find").click(function(){
	find_optimal_routes();
});
get_airports();

