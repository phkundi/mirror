import $ from 'jquery';

class News{
	constructor(){
		this.get_headlines()
	}

	get_headlines(){
		var headline_urls = [
                'http://diepresse.com/rss/Techscience',
                'http://diepresse.com/rss/Wirtschaftsnachrichten',
                'http://diepresse.com/rss/Sport',
                'http://diepresse.com/rss/Politik',
                'http://diepresse.com/rss/Finanzen'
                ]

                var headlines = []

                for (var i = 0; i < headline_urls.length; i++) {
                        $.get(headline_urls[i], function(data){
                                var $xml = $(data);
                                $xml.find('item').each(function(){
                                        var $this = $(this),
                                        item = $this.find('title').text()
                                        headlines.push(item)
                                });
                        });
                }

                console.log(headlines)      
	}
}

export default News;