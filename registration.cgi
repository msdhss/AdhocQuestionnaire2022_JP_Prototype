
#!/usr/bin/perl

# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_JP_prototype/userMan.cgi
# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_JP_prototype/login.cgi
# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_JP_prototype/registration.cgi

# ������
# .users �����Ƥ�õ�
# user.csv�ξõ�
# /answer/����Ȥ�õ�
# /log/����Ȥ�õ�
# /user/����Ȥ�õ�

#== �桼�������� ==
$CHARSET   = 'euc-jp';	# ʸ��������
$USERFILE  = './usrman/.users'; # �桼�����ե�����

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
    printErrorPage("���Υ桼����̾�Ϥ��Ǥ�¸�ߤ��Ƥ��ޤ���");
    }
  $USERS{$name} = $pass;

  # �ѥ���ɤΰŹ沽
  $saltset = 
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789./";
  $n1 = int(rand 64);
  $n2 = ($n1 + time) % 64;
  $salt = substr($saltset, $n1, 1) . substr($saltset, $n2, 1);
  $pass = crypt($pass, $salt);

  # �桼�����˴ؤ������ؽ񤭹���
  # file open
  open(FILE, ">>$USERFILE") or printErrorPage("user file �������ޤ���");
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
  push(@answer,0); # 1: ���ߥ�˥��������ե�������ƿ�
  push(@answer,0); # 2: ������
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
<head><title>�桼������Ͽ�δ�λ</title></head>
<body>
<h1>�桼������Ͽ����λ���ޤ�����</h1>
<p>$_[0]</p>
<meta http-equiv="refresh" content=" 2 ;url= ./userMan.cgi"> 
</body>
</html>
END
  
  exit;

#== �桼�����ե������ɤ߹��� ==
sub loadUserfile
{
  my ($ln, $name, $pass);
  open(FILE, "<$USERFILE")
    or printErrorPage("�桼�����ե����뤬�����ޤ���");
  while($ln = <FILE>) {
    chomp $ln;
    ($name, $pass) = split(/:/, $ln);
    $USERS{$name} = $pass;
  }
  close(FILE);
}

#== ���顼�ڡ������� ====
sub printErrorPage
{
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><title>���󥱡���Ĵ�������ȤؤΥ�������Ͽ</title></head>
<body>
<h1>���顼</h1>
<p>$_[0]</p>
<meta http-equiv="refresh" content=" 2 ;url= ./userMan.cgi"> 
</body>
</html>
END
  
  exit;
}
