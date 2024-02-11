function displayResults(results, store) {
	const searchResults = document.getElementById('results')
	if (results.length) {
		let resultList = ''
		// Iterate and build result list elements
		for (const n in results) {
			const item = store[results[n].ref]
			resultList += '<div class="text-center">'
			resultList += '<h2><a href="' + item.url + '">' + item.title + '</a></h2>'
			resultList += item.content.substring(0, 150) + '...'
			resultList += '<div class="container text-center">'
			item.categories.forEach(t => {
				resultList += '<span class="btn"><i class="fa-duotone theme-fundor333 fa-map-pin"></i> ' + t + '</span>'
			})
			resultList += '</div><div class="container text-center">'
			item.tags.forEach(t => {
				resultList += '<span class="btn"><i class="fa-duotone theme-fundor333 fa-tags"></i> ' + t + '</span>'
			})
			resultList += '</div>'
			resultList += '<hr>'
			resultList += '</div>'
		}
		searchResults.innerHTML = resultList
	} else {
		searchResults.innerHTML = 'No results found.'
	}
}

// Get the query parameter(s)
const params = new URLSearchParams(window.location.search)
const query = params.get('query')

// Perform a search if there is a query
if (query) {
	// Retain the search input in the form when displaying results
	document.getElementById('search-input').setAttribute('value', query)

	const idx = lunr(function () {
		this.ref('id')
		this.field('title', {
			boost: 15
		})
		this.field('tags')
		this.field('content', {
			boost: 10
		})

		for (const key in window.store) {
			this.add({
				id: key,
				title: window.store[key].title,
				tags: window.store[key].category,
				content: window.store[key].content
			})
		}
	})

	// Perform the search
	const results = idx.search(query)
	// Update the list with results
	displayResults(results, window.store)
}
