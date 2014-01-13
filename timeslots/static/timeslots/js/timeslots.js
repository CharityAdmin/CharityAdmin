// timeslots js goes here
$(document).ready(function() {

	// ------------------ //
	// Date Selector Code //
	// ------------------ //

	var $selectorWrapper = $(".js-date-selector");
	var $currentSelectionLabel; // label holding the current-selection
	var $dateMenu; // the menu for the date selector
	var $dateInputs; // the inputs that hold the start and end dates
	var display_date_format; // the format to display dates in
	var label_next30days; // the label for a preselected menu option -- next 30 days
	var startpicker, endpicker, defaultstartdate, defaultenddate;

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
		$selectorWrapper.removeClass("active");

		// start spinner
		// ajax
		// UNTIL THE AJAX IS READY, JUST REFRESHING
		var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?startdate=" + startDate + "&enddate=" + endDate;
		window.location.href = newurl;
		// end spinner

		// Set current-selection label properly
		$currentSelectionLabel.text(label);
	}

	if ($selectorWrapper.length) {
		$currentSelectionLabel = $selectorWrapper.find(".current-selection");
		$dateMenu = $(".js-date-selector-menu");
		$dateInputs = $dateMenu.find(".js-date-input");

		display_date_format = "M/d/yy";
		label_next30days = "Next 30 Days";

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
			window.setTimeout(function() {
				endpicker.show();
			}, 300);
		});

		$dateInputs.eq(1).change(function() {
			activateCustomDate();
		});

		(function determineCurrentSettings() {
			var startDate = Date.parse($(".js-startdate").text());
			var endDate = Date.parse($(".js-enddate").text());
			var label, $currentEl;

			// if startDate and endDate are null or set to startdate=Today and endDate=30 days from now, show the "Next 30 Days"
			if ((startDate === null || Date.equals(startDate, Date.today())) && (endDate === null || Date.equals(endDate, Date.today().add(30).days()))) {
				label = label_next30days;
				$currentEl = $(".js-date-menu-item-next-30-days");
			}
			// else if (false) {
			//// some other potential menu selection would go here
			// }
			else {
				label = startDate.toString(display_date_format) + " to " + endDate.toString(display_date_format);
				$currentEl = $(".js-date-menu-item-custom-dates");
				$dateInputs.eq(0).val(startDate.toString(display_date_format));
				$dateInputs.eq(1).val(endDate.toString(display_date_format));
			}

			defaultstartdate = startDate.toString("yyyy-MM-dd");
			startpicker = new Pikaday({
				field: document.getElementById('startdate'),
				defaultDate: defaultstartdate,
				format: 'MM/DD/YY'
			});
			// startpicker.setDate(defaultstartdate); // THIS CAUSES A REFRESH LOOP BUG

			defaultenddate = endDate.toString("yyyy-MM-dd");
			endpicker = new Pikaday({
				field: document.getElementById('enddate'),
				defaultDate: defaultenddate,
				format: 'MM/DD/YY'
			});
			// endpicker.setDate(defaultenddate); // THIS CAUSES A REFRESH LOOP BUG

			$currentSelectionLabel.text(label);
			$currentEl.addClass("current");
		})();
	}






	// -------------------- //
	// Metadata Editor Code //
	// -------------------- //

	var $editform = $(".form-edit"); // the edit form
	var $typeselector; // the select element that tells us what type of opening/commitment we're dealing with
	var $dateinputgroups; // all the date input control-groups
	var $daysofweekgroup; // the days of week control-group
	var $dayofmonthgroup; // the day of month control-group
	var $oneoffdategroup; // the one-off date control-group
	var oneoffdatepicker; // the date picker for the one-off date control
	var defaultoneoffdate; // the default date string for the date picker
	var editstartdatepicker, editenddatepicker, defaulteditstartdate, defaulteditenddate;
	var editstartdateel, editenddateel; // the start and end date inputs

	function checkEditFormType(timing) {
		switch ($typeselector.val()) {
			case "One-Off":
				switchToDateInputGroup($oneoffdategroup, timing);
				break;
			case "Days of Week":
				switchToDateInputGroup($daysofweekgroup, timing);
				break;
			case "Days of Alt Week":
				switchToDateInputGroup($daysofweekgroup, timing);
				break;
			case "Day of Month":
				switchToDateInputGroup($dayofmonthgroup, timing);
				break;
		}
	}

	function switchToDateInputGroup($dateInputGroup, timing) {
		if (!($dateInputGroup.is(":visible"))) {
			$dateinputgroups.not($dateInputGroup).slideUp(timing, function() {
				$dateInputGroup.slideDown(timing);
			});
		}
	}

	function setupDatePicker(inputElSelector, defaultdate) {
		var inputEl = document.getElementById(inputElSelector);
		if (defaultdate === undefined || defaultdate === "") {
			// fixes with an odd issue with pikaday: https://github.com/dbushell/Pikaday/issues/98
			defaultdate = "Invalid Date";
		}
		var datePicker = new Pikaday({
			field: inputEl,
			defaultDate: defaultdate,
			format: 'MM/DD/YY'
		});
		if (defaultdate !== "Invalid Date") {
			datePicker.setDate(defaultdate);
		}

		return datePicker;
	}

	if ($editform.length) {
		$typeselector = $("#id_type", $editform);
		$daysofweekgroup = $(".control-group-daysOfWeek", $editform);
		$dayofmonthgroup = $(".control-group-dayOfMonth", $editform);
		$oneoffdategroup = $(".control-group-oneOffDate", $editform);
		$dateinputgroups = $daysofweekgroup.add($dayofmonthgroup).add($oneoffdategroup);

		checkEditFormType(5);

		$typeselector.change(function() {
			checkEditFormType(300);
		});

		oneoffdatepicker = setupDatePicker('id_oneOffDate', Date.today(true).toString("yyyy-MM-dd"));
		editstartdatepicker = setupDatePicker('id_startDate_0', $('#id_startDate_0').val());
		editenddatepicker = setupDatePicker('id_endDate_0', $('#id_endDate_0').val());
	}

});