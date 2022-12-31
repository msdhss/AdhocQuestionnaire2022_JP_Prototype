#!/usr/bin/perl

# .../adhocQuestionnaire2022_JP_prototype/userMan.cgi

use CGI;

my $form = new CGI;
print $form->header("text/html");

my $filename = $form->param('uploadFile');

# パス名からファイル名の取り出し
@newfile = split /\\/, $filename;
$newfile = pop @newfile;

# ファイルを保存する。
open (OUTFILE,">$newfile") or die "Can't make serverside file!\n";
while ($bytesread = read($filename,$buffer,1024)) {
  print OUTFILE $buffer;
}

print "O.K. File($filename) was uploaded as $newfile<br>\n";
print "<meta http-equiv='refresh' content=' 2 ;url= ./userMan.cgi'> \n";
