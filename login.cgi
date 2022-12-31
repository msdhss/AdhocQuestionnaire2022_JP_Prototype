#!/usr/bin/perl

# .../adhocQuestionnaire2022_JP_prototype/login.cgi

#== �桼�������� ==
$CHARSET   = 'euc-jp';	# ʸ��������
$USERFILE  = './usrman/.users';	# �桼�����ե�����

#== �ᥤ��ץ���� ==
loadFormdata();
loadUserfile();
  if($FORM{"mode"} eq "adduser") {
    addUser();
  }elsif($FORM{'mode'} eq "deluser") {
    deleteUser();
  }

printAdminPage2();

exit;

#== �桼�����ɲ� ==
sub addUser {
  my ($name, $pass) = ($FORM{'user'}, $FORM{'pass'});
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
  # o file open
  open(FILE, ">>$USERFILE") or printErrorPage("user file �������ޤ���");
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


#== �桼������� ==
sub deleteUser
{
  my ($key, $name);
  
  foreach $key (keys %FORM) {
    if($key =~ /del_(.+)/) {
      delete $USERS{$1};
    }
  }
  
  # �桼�����ե�����񤭹���
  open(FILE, ">$USERFILE")
    or printErrorPage("�桼�����ե����뤬�����ޤ���");
  foreach $name (keys %USERS) {
    print FILE "$name:$USERS{$name}\n";
  }
  close(FILE);
}

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

#== �桼���������ڡ������� ====
sub printAdminPage {
  my $name;
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">

<html>

  <HEAD>
  <META Http-Equiv="Content-Type" Content="text/html; charset=euc-jp">
  <TITLE>���󥱡���Ĵ�������ȤؤΥ��������</TITLE>
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
<h2>���������</h2>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<p>
�桼����̾��
<input type="text" name="user" style="width: 200px; font-size: 0.6em"><br>
<span class="note"> * ����ե��٥å�/�����Τ�</span><br>
<br>
�ѥ���ɡ�&nbsp;
<input type="password" name="pass" style="width: 200px; font-size: 0.6em"><br>
<span class="note"> * ����ե��٥å�/�����Τ�</span>
</p>
<p>
<input type="hidden" name="mode" value="adduser">
<input type="submit" value="��Ͽ����" style="width: 200px; font-size: 1.0em">
</p>
</form>
<hr>
���˥桼������Ͽ�򤷤Ƥ������<a href="./private/top.cgi">������</a>����
<hr>
<br>
�ʤˤ�����������������ޤ����顢msdhss@gmail.com�ޤǤ�Ϣ����������
</div>
</body>
</html>
END
}

#== �桼���������ڡ���2�ν��� ====
sub printAdminPage2 {
  my $name;
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">

<html>

  <HEAD>
  <META Http-Equiv="Content-Type" Content="text/html; charset=euc-jp">
  <TITLE>���󥱡���Ĵ�������ȤؤΥ��������</TITLE>
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
<h2>���������</h2>
<hr>
��Ϣ���Ƥ���桼����̾�ȥѥ���ɤ���Ѥ��ơ�<br>
<p>
������<a href="./private/top.cgi">������</a>����
</p>
�����󤷤Ƥ���������
<hr>
<br>
</div>
</body>
</html>
END
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
<meta http-equiv="refresh" content=" 2 ;url= ./login.cgi"> 
</body>
</html>
END
  
  exit;
}


#== �ե�����ǡ��������� ====
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
# == ��λ�ڡ�����ɽ�� ==
sub Print_Thanks
{
  print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<HTML>
<HEAD><TITLE>�桼������Ͽ���꤬�Ȥ��������ޤ�����</TITLE></HEAD>
<BODY>
<BR>
<center>
<br>
<b>�桼������Ͽ����λ���ޤ�����</b>
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
