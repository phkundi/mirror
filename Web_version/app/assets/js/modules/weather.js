import $ from 'jquery';

class Weather{
	constructor(){
		this.weatherDiv = $('#weather');
		this.get_ip()
	}

	get_ip(){
	    let url = 'http://jsonip.com'
	    
	    $.getJSON(url, (results) => {
	    	this.get_location(results)
	    });

	    // call this function again in 60000ms
	    setInterval(this.get_ip, 60000);
	}

	get_location(data){
		let key = 'b2c0083cd5cabc313e8b70df8580d946' // ipstack api key
		let url = `http://api.ipstack.com/${data.ip}?access_key=${key}`
		console.log(url)

		$.getJSON(url, (results) => {
			this.getWeather(results)
		});
	}

	getWeather(data){
		let location = {
			longitude: data.longitude,
			latitude: data.latitude
		}
		let weather_lang = 'de'
		let weather_unit = 'metric'
		let key = 'b1e84d6ae8596b26aa0ea0f086bc6e30'
		let url = `http://api.openweathermap.org/data/2.5/weather?lat=${location.latitude}&lon=${location.longitude}&units=${weather_unit}&lang=${weather_lang}&appid=${key}` 

		$.getJSON(url, (results) => {
			this.makeHTML(results)
		});
	}

	makeHTML(data){
		var icon_lookup = {
			'01d': 'assets/img/Sun.png',
			'01n': 'assets/img/Moon.png',
			'02d': 'assets/img/PartlySunny.png',
			'02n': 'assets/img/PartlyMoon.png',
			'03d': 'assets/img/Cloud.png',
			'03n': 'assets/img/Cloud.png',
			'04d': 'assets/img/Cloud.png',
			'04n': 'assets/img/Cloud.png',
			'09d': 'assets/img/Rain.png',
			'09n': 'assets/img/Rain.png',
			'10d': 'assets/img/Rain.png',
			'10n': 'assets/img/Rain.png',
			'11d': 'assets/img/Storm.png',
			'11n': 'assets/img/Storm.png',
			'13d': 'assets/img/Snow.png',
			'13n': 'assets/img/Snow.png',
			'50d': 'assets/img/Haze.png',
			'50n': 'assets/img/Haze.png',
		}


		console.log(data)
		this.weatherDiv.html(`
			<span class="temperature">
				${data.main.temp}°</span>
			<span class="icon">
				<img src="${icon_lookup[data.weather[0].icon]}" width='80' height='80'>
			</span>
			<hr class="divider">
			<span class="description">
				${data.weather[0].description}
			</span>
			<span class="location">
				${data.name}
			</span>
		`)
	}


}

export default Weather;