// timeslots js goes here
$(document).ready(function() {

	//
	// Date Selector Code
	//

	var $selectorWrapper = $(".js-date-selector");
	var $currentSelectionLabel = $selectorWrapper.find(".current-selection");
	var $dateMenu = $(".js-date-selector-menu");
	var $dateInputs = $dateMenu.find(".js-date-input");

	var display_date_format = "M/d/yy";
	var label_next30days = "Next 30 Days";

	var startpicker, endpicker;

	$selectorWrapper.on("click", function(e) {
		$selectorWrapper.addClass("active");
		e.stopPropagation();

		$("html").one("click", function(e) {
			$selectorWrapper.removeClass("active");
		});
	});

	$selectorWrapper.hover(function(e) {
		// fixes css transition bug when using :hover css
		$(this).addClass("hover");
	}, function(e) {
		$(this).removeClass("hover");
	});

	$(".js-date-menu-item-custom-dates").click(function(e) {
		e.stopPropagation();

		var $startDate = $dateInputs.eq(0);
		var $endDate = $dateInputs.eq(1);
		var label;

		if ($startDate.val()==="") {
			$startDate.eq(0).focus();
		} else if ($endDate.val()==="") {
			$endDate.focus();
		} else {
			activateCustomDate();
			console.log("activateCustomDate()");
		}
	});

	$(".js-date-menu-item-next-30-days").click(function(e) {
		e.stopPropagation();
		setDateRange(label_next30days, Date.today().toISOString(), Date.today().add(30).days().toISOString());
	});

	$dateInputs.click(function(e) {
		e.stopPropagation();
	});

	$dateInputs.focus(function() {
		$dateMenu.addClass("date-selection-active");

		$("html, .js-date-selector").one("click", function(e) {
			$dateMenu.removeClass("date-selection-active");
		});
	});

	$dateInputs.eq(0).change(function() {
		$dateInputs.eq(1).focus();
		console.log("SHOW!");
		console.log(endpicker);
		window.setTimeout(function() {
			endpicker.show();
		}, 300)
	});

	$dateInputs.eq(1).change(function() {
		activateCustomDate();
	});

	function activateCustomDate() {
		var $startDate = $dateInputs.eq(0);
		var $endDate = $dateInputs.eq(1);
		var startDateVal, endDateVal, startDateObj, endDateObj, startDateText, endDateText;
		var label;

		if (($startDate.val()!=="") && ($endDate.val()!=="")) {
			startDateText = $startDate.val();
			startDateObj = Date.parse(startDateText);
			endDateText = $endDate.val();
			endDateObj = Date.parse(endDateText);

			startDateVal = startDateObj.toString(display_date_format);
			endDateVal = endDateObj.toString(display_date_format);
			label = startDateVal + " to " + endDateVal;

			setDateRange(label, startDateObj.toISOString(), endDateObj.toISOString());
		}
	}

	function setDateRange(label, startDate, endDate) {
		// Takes Date Selector Label and startDate and endDate as ISO Date strings
		console.log("Start Date: ");
		console.log(startDate);
		console.log("End Date: ");
		console.log(endDate);

		$selectorWrapper.removeClass("active");

		// start spinner
		// ajax
		// UNTIL THE AJAX IS READY, JUST REFRESHING
		console.log(window.location.hostname);
		console.log(window.location.pathname);
		var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?startdate=" + startDate + "&enddate=" + endDate;
		window.location.href = newurl;
		console.log(newurl);

		// end spinner

		// Set current-selection label properly
		console.log(label);
		console.log($currentSelectionLabel);
		$currentSelectionLabel.text(label);
	}

	(function determineCurrentSettings() {
		var startDate = Date.parse($(".js-startdate").text());
		var endDate = Date.parse($(".js-enddate").text());
		var label, $currentEl;

		console.log("COMPARE DATES");
		// console.log(startDate);
		// console.log(Date.today());
		// console.log(Date.equals(startDate, Date.today()));

		// console.log(endDate);
		// console.log(Date.today().add(30).days());
		// console.log(Date.equals(endDate, Date.today().add(30).days()));

		// if startDate and endDate are null or set to startdate=Today and endDate=30 days from now, show the "Next 30 Days"
		if ((startDate === null || Date.equals(startDate, Date.today())) && (endDate === null || Date.equals(endDate, Date.today().add(30).days()))) {
			label = label_next30days;
			$currentEl = $(".js-date-menu-item-next-30-days");
		}
		// else if (false) {
		// 	// some other potential menu selection would go here
		// }
		else {
			label = startDate.toString(display_date_format) + " to " + endDate.toString(display_date_format);
			$currentEl = $(".js-date-menu-item-custom-dates");
			$dateInputs.eq(0).val(startDate.toString(display_date_format));
			$dateInputs.eq(1).val(endDate.toString(display_date_format));
		}

		startpicker = new Pikaday({
			field: document.getElementById('startdate'),
			defaultDate: startDate.toString("yyyy-mm-dd"),
			format: 'MM/DD/YY'
		});

		endpicker = new Pikaday({
			field: document.getElementById('enddate'),
			defaultDate: endDate.toString("yyyy-mm-dd"),
			format: 'MM/DD/YY'
		});

		$currentSelectionLabel.text(label);
		$currentEl.addClass("current");
	})();

	// determineCurrentSettings();

});