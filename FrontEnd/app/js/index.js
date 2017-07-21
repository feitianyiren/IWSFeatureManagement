function AppViewModel(){
	this.yourName = ko.observable("");
}

ko.applyBindings(new AppViewModel());