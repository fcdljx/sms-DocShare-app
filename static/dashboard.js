//code in this block executes after the page has loaded
$(document).ready(function () {
	populateList(items)
	console.log("hiii im here")
})

function populateList(item){
  $("#overall-data").html("")
  // var count = 1
  items.forEach(function (item) {
    let session_id = item['id']
    let time_last_seen = item['time_last_seen']

		//some jQuery + bootstrap for new frontend rows/columns
		let newRow = $("<div>", { "class": "row text-center", "id": session_id });
		let sessionColumn = $("<div>", { "class": "col-6 text-center data" });
		sessionColumn.html(session_id)
		let timeColumn = $("<div>", { "class": "col-6 text-center data" });
		timeColumn.html(time_last_seen)

		//add all the new DOM elements to a row
		newRow.append(sessionColumn)
		newRow.append(timeColumn)

		//when you click the textColumn, go to the corresponding individual data
		sessionColumn.click(function () {
			singleData(session_id)
		})

		// append the row to the page
		$("#overall-data").append(newRow)
		});
}

//function to make POST request to update item in firestore
function singleData(session_id) {
	url1 = "/display_user_data/<"
	url_str = url1.concat(session_id,">")

	window.location.href = url_str ;
}
