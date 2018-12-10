class Time{
	constructor(){
		this.updateClock();
	}

	updateClock() {
	    var now = new Date() // current date
	    var months = [
	        			'Januar', 
	        			'Februar', 
	        			'März', 
	        			'April', 
	        			'Mai', 
	        			'Juni', 
	        			'Juli', 
	        			'August', 
	        			'September', 
	        			'Oktober', 
	        			'November', 
	        			'Dezember'
	        ];

	    var time = now.toLocaleTimeString('de-DE', {hour: 'numeric', minute: 'numeric'});
	    var date = now.toLocaleDateString('de-DE');
	    var weekdays_lookup = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
	    var weekday = weekdays_lookup[now.getDay()];

	    document.getElementById('time').textContent = time;
	    document.getElementById('date').textContent = weekday + ', ' + date

	    // call this function again in 1000ms
	    setInterval(this.updateClock, 1000);
	}
}

export default Time;