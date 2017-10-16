/**
 * Created by OXOYO on 2017/10/13.
 */
const fs = require('fs')
var cheerio = require('cheerio')

var html = fs.readFileSync('./bookmarks.html')
var $ = cheerio.load(html)
var readmeContent = ''
var writeFile = function (fileName, content) {
    var filePath = './md/'
    // 写入文件
    fs.writeFile(filePath + fileName, content, function (err) {
        if (err) {
            return console.error(err)
        } else {
            console.log(fileName + ' created success!')
        }
    })
}

$('h3').each(function(i, el) {
    var node = $(el)
    if (!node.attr('personal_toolbar_folder')) {
        console.log('PERSONAL_TOOLBAR_FOLDER', node.text())
        var content = '## ' + node.text() + '\n\n'
        var childContent = ''
        node.next().find('a').each(function(i, el) {
            var child = $(el)
            var childText = child.text()
            var childHref = child.attr('href')
            childContent += '[' + childText + '](' + childHref + ')' + '\n\n'

            var nextH3 = child.parent().next().find('h3')
            if (nextH3.text()) {
                console.log('h3', nextH3.text())
                return false
            }
        })
        content += childContent
        readmeContent += content
        var fileName = node.text() + '.md'
        // 写入相应的md文件
        writeFile(fileName, content)
    }
})

// 写入README.md
writeFile('README.md', readmeContent)