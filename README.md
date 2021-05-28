# douban_comment
This program is making for getting shot-comment-information from movie.douban.com.
## Some words
In fact, this program is just a homework. But when I finished coding my program, I found that it seems can be a tool to getting every movie's shot-comment-information.

正直言って、私は英語があまり使えない。ときどき頭の中で日本語を自動翻訳して。でも、英語試験があるんだ、我慢して！

所以使用中日英三语留言都是ok的
## Help
First, you need to make a url list, as 'url_list.txt'. If you save that file with wrong url or format, the program will report an error.

Second, you need to refresh your own cookie and user-agent in 'cookie.txt' and 'user_agent.txt'.

Third, 'Python 3.9(32-bit)'.

Forth, I exchanged all of r'\n' to r'\s' in comments.

Fifth, csv package may show you '###' in column 'comment_time' and '&#34' in column 'comment'.
