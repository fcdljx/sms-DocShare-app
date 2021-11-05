//code in this block executes after the page has loaded
$(document).ready(function () {
	getNumber(user_id)
	populateList(items)
	console.log("hiii im here")
})

function getNumber(user_id){
  $("#session-number").html("")
	let session = user_id
	let textColumn = $("<div>", { "class": "col-12 text-center data" });
	textColumn.html(session)

	$("#session-number").append(textColumn)
}

function populateList(item){
  $("#overall-data").html("")
  var count = 1

  items.forEach(function (item) {
    // let question_id = item['id']
    let text = item['text']

		//some jQuery + bootstrap for new frontend rows/columns
		let newRow = $("<div>", { "class": "row text-center"});
		let textColumn = $("<div>", { "class": "col-6 text-center data" });
		textColumn.html(text)

		//add all the new DOM elements to a row
		// newRow.append(idColumn)
    newRow.append(textColumn)

		// append the row to the page
		$("#overall-data").append(newRow)
    count +=1
		});
}
