#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # form data の取得して、$in{}に収納
# 環境編集の取得
$user_name = $ENV{'REMOTE_USER'};
# Web表示とアンケートの送信と分析
    print "Content-type: text/html\n\n";
    print qq!
    <HTML>
    <HEAD>
    <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
    <TITLE>Dynamic Evaluation</TITLE>
    </HEAD>
    <BODY>
    <div align="left">${UserName()}</div>
    <hr>
    !;
&Print_Thanks;
    print qq!
	</BODY>
	</HTML>
    !;
	exit;
# end
##############################
### ユーザネーム
##############################
sub UserName
{
    print "ユーザ : $user_name";
    print "　　<a href='./mobile_top.cgi'>Top</a>";
}
##############################
### データ表示
#############################
sub Print_Thanks
{
    print qq!
<h2>今までの評価</h2>
	!;
# i file open
    $i = $user_name.".dat";
    open(IN, "./user/$i");
    <IN>; # line 1 throw
    @data = <IN>;
    close(IN);
    open(STORE, "./store_list.dat");
    @store = <STORE>;
    close(STORE);
    if(!$data[0]){ # $data[0] に評価データがない場合
	print "まだ評価をしていません\n";
    }else{ # $data[0] に評価データが存在する場合
	foreach(@data){
	    chomp();
	    @subdata = split(/\t/);
	    print "　　店舗名: $subdata[0]　利用回数 $subdata[1]　使用したお金 $subdata[2]　期待 $subdata[4]　期待からのずれ $subdata[5]　満足度 $subdata[6]　 コメント: $subdata[7]　日時: $subdata[8] <br>\n";
	}
    }
}
