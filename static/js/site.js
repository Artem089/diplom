let phoneInput = document.querySelector(".phone-number-mask");
if (phoneInput) {
	const phoneMask = new IMask(phoneInput, {
		mask: "{8} (000) 000-00-00",
	});
}
