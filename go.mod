module github.com/fundor333/fundor333.github.io

go 1.22.5

require (
	github.com/fundor333/macha-theme v0.0.0-20240812172411-2909033aceb7 // indirect
	github.com/fundor333/macia-image v0.0.0-20240728183659-e648e0050a87 // indirect
	github.com/fundor333/macia-indiweb v0.0.0-20240728170323-78be1951ae2d // indirect
)

// For local theme development, you can use replace directives to change the
// location of a loaded module. For instance, to change the location of the
// rootwork/hugo-clarity module, uncomment the next section and change the local
// path to a valid directory relative to this file. Then run `hugo mod get` on
// the command line. More info:
// https://github.com/rootwork/hugo-module-site#local-theme-development

// replace github.com/fundor333/fugu-theme => /Users/matteoscarpa/Coding/Personale/fugu-theme
replace github.com/fundor333/macha-theme => /Users/matteoscarpa/Coding/Personale/macia-theme
