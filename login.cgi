#!/usr/bin/perl

# .../adhocQuestionnaire2022_JP_prototype/login.cgi

#== ユーザー設定 ==
$CHARSET   = 'euc-jp';	# 文字コード
$USERFILE  = './usrman/.users';	# ユーザーファイル

#== メインプログラム ==
loadFormdata();
loadUserfile();
  if($FORM{"mode"} eq "adduser") {
    addUser();
  }elsif($FORM{'mode'} eq "deluser") {
    deleteUser();
  }

printAdminPage2();

exit;

#== ユーザー追加 ==
sub addUser {
  my ($name, $pass) = ($FORM{'user'}, $FORM{'pass'});
  my ($salt, $saltset, $n1, $n2);
	
  if(exists $USERS{$name}) {
    printErrorPage("そのユーザー名はすでに存在しています。");
  }
  $USERS{$name} = $pass;
	
  # パスワードの暗号化
  $saltset = 
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789./";
  $n1 = int(rand 64);
  $n2 = ($n1 + time) % 64;
  $salt = substr($saltset, $n1, 1) . substr($saltset, $n2, 1);
  $pass = crypt($pass, $salt);
	
  # ユーザーに関する情報へ書き込み
  # o file open
  open(FILE, ">>$USERFILE") or printErrorPage("user file が開けません");
  $i = $name.".log";
  open(USER, ">>./private/user/$i");
  # management
  print FILE "$name:$pass\n";
  # o file close
  close(FILE);
  close(USER);
  # transfer to evaluation page
  Print_Thanks();
}


#== ユーザー削除 ==
sub deleteUser
{
  my ($key, $name);
  
  foreach $key (keys %FORM) {
    if($key =~ /del_(.+)/) {
      delete $USERS{$1};
    }
  }
  
  # ユーザーファイル書き込み
  open(FILE, ">$USERFILE")
    or printErrorPage("ユーザーファイルが開けません。");
  foreach $name (keys %USERS) {
    print FILE "$name:$USERS{$name}\n";
  }
  close(FILE);
}

#== ユーザーファイル読み込み ==
sub loadUserfile
{
  my ($ln, $name, $pass);
  
  open(FILE, "<$USERFILE")
    or printErrorPage("ユーザーファイルが開けません。");
  while($ln = <FILE>) {
    chomp $ln;
    ($name, $pass) = split(/:/, $ln);
    $USERS{$name} = $pass;
  }
  close(FILE);
}

#== ユーザー管理ページ出力 ====
sub printAdminPage {
  my $name;
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">

<html>

  <HEAD>
  <META Http-Equiv="Content-Type" Content="text/html; charset=euc-jp">
  <TITLE>アンケート調査サイトへのログイン画面</TITLE>
  <style type="text/css">
    div#container {
      width: 650px; margin-left: auto; margin-right: auto; 
        font-size: 1.3em}
    div#container td {font-size: 3.5em}
    div#contents {
      width: 650px; 
        margin-left: auto; margin-right: auto; font-size: 1em}
    div#header {
      width: 650px; margin-left: auto; margin-right: auto; font-size: 1em}
    span.note {font-size: 0.5em}
    </style>
  </HEAD>

<body>
<div id="container">
<h2>ログイン画面</h2>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<p>
ユーザー名：
<input type="text" name="user" style="width: 200px; font-size: 0.6em"><br>
<span class="note"> * アルファベット/数字のみ</span><br>
<br>
パスワード：&nbsp;
<input type="password" name="pass" style="width: 200px; font-size: 0.6em"><br>
<span class="note"> * アルファベット/数字のみ</span>
</p>
<p>
<input type="hidden" name="mode" value="adduser">
<input type="submit" value="登録する" style="width: 200px; font-size: 1.0em">
</p>
</form>
<hr>
既にユーザー登録をしている場合は<a href="./private/top.cgi">こちら</a>から
<hr>
<br>
なにかご不明な点がありましたら、msdhss@gmail.comまでご連絡ください。
</div>
</body>
</html>
END
}

#== ユーザー管理ページ2の出力 ====
sub printAdminPage2 {
  my $name;
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">

<html>

  <HEAD>
  <META Http-Equiv="Content-Type" Content="text/html; charset=euc-jp">
  <TITLE>アンケート調査サイトへのログイン画面</TITLE>
  <style type="text/css">
    div#container {
      width: 650px; margin-left: auto; margin-right: auto; 
        font-size: 1.3em}
    div#container td {font-size: 3.5em}
    div#contents {
      width: 650px; 
        margin-left: auto; margin-right: auto; font-size: 1em}
    div#header {
      width: 650px; margin-left: auto; margin-right: auto; font-size: 1em}
    span.note {font-size: 0.5em}
    </style>
  </HEAD>

<body>
<div id="container">
<h2>ログイン画面</h2>
<hr>
ご連絡してあるユーザー名とパスワードを使用して、<br>
<p>
　　　<a href="./private/top.cgi">こちら</a>から
</p>
ログインしてください。
<hr>
<br>
</div>
</body>
</html>
END
}

#== エラーページ出力 ====
sub printErrorPage
{
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><title>アンケート調査サイトへのログイン登録</title></head>
<body>
<h1>エラー</h1>
<p>$_[0]</p>
<meta http-equiv="refresh" content=" 2 ;url= ./login.cgi"> 
</body>
</html>
END
  
  exit;
}


#== フォームデータ取り込み ====
sub loadFormdata
{
  my ($query, $pair);
  
  if($ENV{'REQUEST_METHOD'} eq 'POST') {
    read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
  }
  else {
    $query = $ENV{'QUERY_STRING'};
  }
  
  foreach $pair (split(/&/, $query)) {
    my ($key, $value) = split(/=/, $pair);
    
    $value =~ tr/+/ /;
    $value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
    
    $FORM{$key} = $value;
  }
}
# == 完了ページの表示 ==
sub Print_Thanks
{
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<HTML>
<HEAD><TITLE>ユーザー登録ありがとうございました。</TITLE></HEAD>
<BODY>
<BR>
<center>
<br>
<b>ユーザー登録が完了しました。</b>
<br>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ./private/top.cgi"> 
</center>
<P>
</BODY>
</HTML>
END

  exit;
}
