#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # related to cgi-lib.pl
# 
$user_name = $ENV{'REMOTE_USER'};
# 
&Print_Thanks;
# 
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>Dynamic Evaluation</TITLE>
<style type="text/css">
a {color: #017acd}
table {width: 880px; font-size: 0.8em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 3.0em}
</style>
</HEAD>
<BODY>
<div id="container">
<div id="header">
ユーザ: $user_name
<a href='./mobile_top.cgi'>Top</a>
</div>
<hr>
<table class="table" border="4">
 <tr><th>日時</th><th>利用店舗</th><th>使用金額</th><th>サービス</th></tr>
 !;
    &Log;
    print qq!
</table>
<hr>
</div>
</BODY>
</HTML>
	!;
	exit;
}
#
# StoreSort
#
sub Log
{
# initialize of sort file
    open(IN, "./user/$user_name.log") or die "Cannot open file\n";
    <IN>;
    @data = <IN>;
    close(IN);
#
    open(STORE, "./store_list.dat") or die "Cannot open file\n";
    @store_name = <STORE>;
    close(STORE);
#
    @data = reverse(@data);
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	foreach $name (@store_name){
	    chomp($name);
	    @substore_name = split(/\t/, $name);
	    if($subdata[1]==$substore_name[0]){
		$subdata[1]=$substore_name[1];
	    }
	}
	print "<tr><td>$subdata[1]</td><td>$subdata[2]</td><td>$subdata[3]</td><td>$subdata[4]</td></tr>\n";
    }
}
