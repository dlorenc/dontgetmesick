function required()
{
	var empt1 = document.forms.SickForm.sick_person_name.value;
	var empt2 = document.forms.SickForm.sick_person_email.value;
	var empt3 = document.forms.SickForm.boss_email.value;
	if (empt1 === "" || empt2 === "" || empt3 === "")
	{
		alert("Please fill out all fields");
		return false;
	}
	else
	{
		return true;
	}
}