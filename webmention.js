const fs = require("fs");
const https = require("https");
const path = require('path');

function writeFileSyncRecursive(filename, content = '') {
	fs.mkdirSync(path.dirname(filename), { recursive: true })
	fs.writeFileSync(filename, content)
}

fetchWebmentions().then(webmentions => {
	webmentions.forEach(webmention => {
		const slug = webmention["wm-target"]
			.replace("https://fundor333.com/", "")
			.replace(/\/$/, "").split('?')[0];

		const filename = `${__dirname}/data/webmentions/${slug}.json`;

		if (!fs.existsSync(filename)) {
			writeFileSyncRecursive(filename, JSON.stringify([webmention], null, 2));

			return;
		}

		const entries = JSON.parse(fs.readFileSync(filename))
			.filter(wm => wm["wm-id"] !== webmention["wm-id"])
			.concat([webmention]);

		entries.sort((a, b) => a["wm-id"] - b["wm-id"]);

		fs.writeFileSync(filename, JSON.stringify(entries, null, 2));
	});
});



function fetchWebmentions() {
	const token = "-g5vlz9y3p5llrdS7TmnCg";

	const since = new Date();
	since.setDate(since.getDate() - 30);

	const url =
		"https://webmention.io/api/mentions.jf2" +
		"?domain=fundor333.com" +
		`&token=${token}` +
		`&since=${since.toISOString()}` +
		"&per-page=999";

	return new Promise((resolve, reject) => {
		https
			.get(url, res => {
				let body = "";

				res.on("data", chunk => {
					body += chunk;
				});

				res.on("end", () => {
					try {
						resolve(JSON.parse(body));
					} catch (error) {
						reject(error);
					}
				});
			})
			.on("error", error => {
				reject(error);
			});
	}).then(response => {
		if (!("children" in response)) {
			console.log(response);
			throw new Error("Invalid webmention.io response.");
		}

		return response.children;
	});
}
