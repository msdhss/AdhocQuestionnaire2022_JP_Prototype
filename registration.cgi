
#!/usr/bin/perl

# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_JP_prototype/userMan.cgi
# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_JP_prototype/login.cgi
# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_JP_prototype/registration.cgi

# 初期条件
# .users の内容を消去
# user.csvの消去
# /answer/の中身を消去
# /log/の中身を消去
# /user/の中身を消去

#== ユーザー設定 ==
$CHARSET   = 'euc-jp';	# 文字コード
$USERFILE  = './usrman/.users'; # ユーザーファイル

loadUserfile();

open(IN,"user.csv") or "die\n";
  @data = <IN>;
close(IN);

foreach(@data){
  chomp($_);
  @subdata = split(/,/,$_);
  my ($name, $pass) = ($subdata[0], $subdata[1]);
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
  # file open
  open(FILE, ">>$USERFILE") or printErrorPage("user file が開けません");
  $i = $name.".log";
  open(USER1, ">./private/log/$i");
  open(USER2, ">./private/user/$i");
  open(IND, ">./private/answer/$i");
  open(IND2, ">./private/communication/$i");
  # management
  print FILE "$name:$pass\n";
  print USER1 "$name:$pass\n";
  @answer = ();
  push(@answer,$name); # 0: user_name
  push(@answer,0); # 1: コミュニケーションファイル投稿数
  push(@answer,0); # 2: 回答数
  print USER2 join("\t",@answer)."\n";
  print IND $name."\n";
  print IND2 $name."\n";
  # file close
  close(FILE);
  close(USER1);
  close(USER2);
  close(IND); 
  close(IND2);
  }

  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><title>ユーザー登録の完了</title></head>
<body>
<h1>ユーザー登録が完了しました。</h1>
<p>$_[0]</p>
<meta http-equiv="refresh" content=" 2 ;url= ./userMan.cgi"> 
</body>
</html>
END
  
  exit;

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
<meta http-equiv="refresh" content=" 2 ;url= ./userMan.cgi"> 
</body>
</html>
END
  
  exit;
}
