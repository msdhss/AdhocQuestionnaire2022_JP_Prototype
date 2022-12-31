#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # $in{'name'} which are included form data
&WebQ; 
# main script
sub WebQ{
# user name ---------------------------------------------------------------------------
    $user_name = $ENV{'REMOTE_USER'};
    $dir = $user_name.".log";
    open(IN, "../../../../../user/$dir") or die "cannot open the file\n";
    @data = <IN>;
    close(IN);
    if($data[0] =~ /1/){
	$maxindex = @data - 1;
	@subdata = split(/\t/,$data[$maxindex]);
	$id_answer = $subdata[0] + 1;
    }else{
    $id_answer = 1;
    }
# store dir name ---------------------------------------------------------------------------
    @script_url = split(/\//,$ENV{"SCRIPT_NAME"});
    $store_region = $script_url[3].$script_url[4].$script_url[5].$script_url[6]; 
    $store_address = $script_url[3].$script_url[4].$script_url[5].$script_url[6].$script_url[7]; 
    open(DATA, "../storelist_$store_region.dat") or die "cannot open the file\n";
    @data = <DATA>;
    close(DATA);
     foreach(@data){
	 chomp($_);
	 @subdata = split(/\t/, $_);
	 if($subdata[0] =~ /$store_address/){
	     $store_name = $subdata[3];
	 }
     }
# date ---------------------------------------------------------------------------
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900;
	$mon += 1;
	my($date) = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
# first time or more than 2nd time? -----------------------------------------------
    unless($in{'first'}=="3"){
    $i = $user_name.".dat";
    open(DATE, "../../../../../user/$i") or die "can not open file\n";
    @data = <DATE>;
    close(DATE);
    $count = 0; # first or not
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/,$_);
	if($subdata[0] =~ /$store_address/){
	    $count += 1;
	}else{
	    $count += 0;
	}
    }
# in the case of first evaluation, �о�Ź�ޤ����Ѥ����Ƥ��������Ǥʤ�����Ƚ��
    if($count == 10){#�������ή���ʤ�
	if($in{'first'}=="1"){
	    $count = 0;
	}elsif($in{'first'}=="2"){
	    $count = 1;
	}else{
	&DivideFirst();
        }
    }else{}
}
# in the case of putting ANSER  
    if($in{"answer"}){
	push(@answer,$id_answer);
	push(@answer,$in{"a1"});
	push(@answer,$store_name);
	$money = $in{"a2_1"}.$in{"a2_2"}.$in{"a2_3"}.$in{"a2_4"}.$in{"a2_5"};
	$find = index($money,"0");
	if($find == 0){
	    substr($money,0,1)="";
	    $find = index($money,"0");
	    if($find == 0){
		substr($money,0,1)="";
		$find = index($money,"0");
		if($find == 0){
		    substr($money,0,1)="";
		    $find = index($money,"0");
		    if($find == 0){
			substr($money,0,1)="";
			$find = index($money,"0");
		    }
		}
	    }
	}
	push(@answer,$money);
	push(@answer,$in{"a3"});
	push(@answer,$in{"a4"});
	push(@answer,$date);
	if(open(OFILE,">>answer.log")){
	   print OFILE join("\t",@answer)."\n";
	   close(OFILE); 
# idividual data
	   open(IND, ">>../../../../../user/$user_name.log");
	   print IND join("\t",@answer)."\n";
	   close(IND); 
# transform char to num
			&ToNum; #���󥱡��Ȥη�̤�ǡ����ե�������Ѵ�(evaluation_number.dat)
			&SubData; #�������ִ������ǡ��������Ѳ�����Ȥ˶�ʬ(data_$i.dat)
			&MeanVariance; #���Ѳ����ʬ�ǡ���(data_$i.dat)��ʿ�Ѥ�ʬ����Ȥ�Ʊ��ե�����(data_figure.gp)�ˤޤȤ��
			system "/home/msdhss/bin/gnuplot 'figure.gp'"; # gnuplot��batch�ե�����μ¹�gnuplot�ξ������Хѥ��ǻ���
			&Print_Thanks; #���󥱡��Ȥδ�λ�ڡ����ν��Ϥǥץ����ν�λ	
		} else {
			&Print_Error("�ե�����ν���˼��Ԥ��ޤ�����");
		}
}
#--------------------------------------------------------------------------
# ���󥱡��ȥڡ����� HTML -------------------------------------------------
#--------------------------------------------------------------------------
print "Content-type: text/html\n\n";
#�����ȥ�
print qq!
<HTML>
<HEAD>
	<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
	<TITLE>$store_name��ɾ��</TITLE>
<style>
div#container{width: 750px; margin-left: auto; margin-right: auto; font-size: 2.5em}
div#container td {font-size: 3.5em}
div#header{width: 750px; margin-left: auto; margin-right: auto; font-size: 2.8em}
</style>
</HEAD>
<BODY>
<div id=container>
${&UserName}
<CENTER>
<FORM ACTION="evaluation.cgi" METHOD="POST">
<TABLE>
<font size=4>
<tr><td><B>��1��</B></td><td><b>��������</b></td></tr>
<tr><td></td><td>
<select name="a1" style="width: 400px; font-size: 0.7em">
!;
    for($i=60;$i>0;$i--){
    $t = time;
    $t -= $i*60*60*24;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($t);
    $year += 1900;
    $mon += 1;
    $list_date = sprintf("%04d/%02d/%02d", $year, $mon, $mday);
print qq!
<option value="$list_date">$list_date
!;
}
    $t = time;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($t);
    $year += 1900;
    $mon += 1;
    $list_date_today = sprintf("%04d/%02d/%02d", $year, $mon, $mday);
print qq!
<option value="$list_date_today" selected>$list_date_today
</select></td></tr>
<tr><td><B>��2��</B></td><td><b>���Ѷ��</b></td></tr>
<tr><td></td><td>
!;
    for($i=1; $i<6; $i++){
	print "<select name='a2_$i' style='font-size: 0.7em'>\n";
	for($j=0; $j<10; $j++){
	    print "<option value='$j'>$j</option>\n";
	}
	print "</select>\n";
    }
print qq!
<b>��</b>
</td></tr>
<tr><td><B>��3��</B></td><td><b>�󶡤��줿�����ӥ�</b></td></tr>
<tr><td></td><td>
<select name="a3" style='width: 400px; font-size: 0.7em'>
 <option value="N/A">���򤷤Ƥ�������</option>
 <option value="���Ԥ򤫤ʤ���ä�">���Ԥ򤫤ʤ���ä�</option>
 <option value="���Ԥ�����ä�">���Ԥ�����ä�</option>
 <option value="�����̤�">�����̤�</option>
 <option value="���Ԥ��䲼��ä�">���Ԥ��䲼��ä�</option>
 <option value="���Ԥ򤫤ʤ겼��ä�">���Ԥ򤫤ʤ겼��ä�</option>
</select>
</td></tr>
<tr><td><B>��4��</B></td><td><b>��­��</b></td></tr>
<tr><td></td><td>
<select name="a4" style='width: 400px; font-size: 0.7em'>
 <option value="N/A">���򤷤Ƥ�������</option>
 <option value="������­">������­</option>
 <option value="�����­">�����­</option>
 <option value="�ɤ���Ȥ⤤���ʤ�">�ɤ���Ȥ⤤���ʤ�</option>
 <option value="�������">�������</option>
 <option value="��������">��������</option>
</select>
</td></tr>
</font>
</TABLE>
<br>
	<P>
		<INPUT TYPE="hidden" NAME="first" VALUE="3">
		<INPUT TYPE="hidden" NAME="number" VALUE="$number">
		<INPUT TYPE="submit" NAME="answer" VALUE="ɾ��������" style="font-size: 1em">
	</FORM>
        <p>
		</CENTER>
</div>
</BODY>
</HTML>
!;
    }
# top bar
sub UserName
{
    print "<div id='header'>";
    print "�桼�� : $user_name��";
    print "<a href='../../../../../mobile_top.cgi'>Top</a><hr>";
    print "</div>";
}
# �����ӥ��ν�����Ѥ��������֤����ѲĤ�Ƚ��
sub DivideFirst
{
    print "Content-type: text/html\n\n";
    print qq!
	<html>
	 <head>
	  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
	  <titel>���Ƥ����� or ʣ��������</title>
	 </head>
	 <body>
	  <form action="evaluation.cgi" method="post">
	  ���Ƥ�����<INPUT TYPE="submit" NAME="first" VALUE="1"><br>
	  ���ƤǤϤʤ�<INPUT TYPE="submit" NAME="first" VALUE="2"><br>
	  </form>
	 </body>
	</html>
	!;
    exit;
}
#
# ���顼�ڡ�����ɽ�� 
#
sub Print_Error
{
	my($error) = @_;
	print "Content-type: text/html\n\n";
	print qq!
	<HTML>
	<HEAD>
		<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
		<TITLE>���顼��ȯ�����ޤ���</TITLE>
	</HEAD>
	<BODY>
		<BR>
		<B>���顼��ȯ�����ޤ���</B>
		<P>
		$error<BR>
		<P>
		�����ȱ��ļԤˤ��䤤�礻��������<BR>
	</BODY>
	</HTML>
	!;
	exit;
}
# ��λ�ڡ�����ɽ�� ---------------------------------------------------------------------------
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>���������꤬�Ȥ��������ޤ�����</TITLE>
</HEAD>
<BODY>
<BR>
<center>
<br>
<b>ɾ���ǡ�������������λ���ޤ�����</b>
<br>
<b>��ưŪ��<a href="../../../../../mobile_top.cgi">HP</a>�����ޤ���</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ../../../../../mobile_top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}
# ���󥱡��ȷ�̤�������ִ�  ---------------------------------------------------------------------------
sub ToNum
{
# i/o file open
    open(IN, "evaluation.log") or die "can not open file\n"; # initial ��������
    open(OUT, ">evaluation.dat") or die "can not open file for writing\n"; # initial ��������
    open(FIG, ">>evaluation_number.dat") or die "can not open file for writing\n"; # evaluation_number.dat��intial������
# User file open
    $i = $user_name.".dat";
    open(USER, ">>../../../../../user/$i") or die "can not open file for writing\n"; # initial ��������
#
# management
#
    $,="\t"; #printf ��ʸ�����ڤ��Ⱦ��space��
    $total_number = 0; #��ɾ�����Υ������
# evaluatio.log �� @dat �˼�Ǽ
    while(<IN>){
	$total_number += 1;
	chomp;
	@dat=split(/\t/);
	print OUT $user_name, $dat[0], $dat[1], $dat[2], $dat[3],$dat[4], $dat[5], $dat[6], $dat[7], "\n";
    }
# �ǥ��쥯�ȥ�̾�γ���
    @script = split(/\//,$ENV{"SCRIPT_NAME"});
    $store_address = $script[3].$script[4].$script[5];
# total_evaluation_number.dat �κ���
    open(TOTALIN, "../total_evaluation_number.dat"); #���Ƥ�Ź��̾��ɾ�����Υե�����
    @data = <TOTALIN>;
    close (TOTALIN);
    open(TOTALOUT, ">../total_evaluation_number.dat"); 
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	if($subdata[0] =~ /$store_address/){ 
	    print TOTALOUT "$store_address\t$total_number\n";
	}else{
	    print TOTALOUT  "$subdata[0]\t$subdata[1]\n";
	}
    }
    close(TOTALOUT);
# comment.dat �κ���
    open(COMMENT, ">>./comment.dat");
    print COMMENT $user_name, $dat[0], $dat[5], $dat[6], "\n";
    close(COMMENT);
# evaluation.dat ��ޤ�ɽ�����뤿��˿��ͥǡ������ִ�������ɬ�ס�perl ���ִ�����
    print FIG "$user_name\t";
    print USER "$script_url[3]$script_url[4]$script_url[5]\t";
## Question 1: a number of timesradio
    if(!$dat[0]){
	$subdat = "\t";
    }elsif($dat[0]=~/����/){
	$subdat = "1\t";
    }elsif($dat[0]=~/2�󤫤�4��/){
	$subdat = "2\t";
    }elsif($dat[0]=~/5�󤫤�7��/){
	$subdat = "3\t";
    }elsif($dat[0]=~/8�󤫤�10��/){
	$subdat = "4\t";
    }elsif($dat[0]=~/11�󤫤�13��/){
	$subdat = "5\t";
    }elsif($dat[0]=~/14��ʾ�/){
	$subdat = "6\t";
    }else{
	$subdat = "\t";
    }
    print FIG $subdat;
    print USER $subdat;
## Question 2: ����
			if(!$dat[1]){
			    print FIG "\t";
			    print USER "\t";
			}elsif($dat[1]=~/���˴���/){
			    print FIG "5\t";
			    print USER "5\t";
			}elsif($dat[1]=~/������/){
			    print FIG "4\t";
			    print USER "4\t";
			}elsif($dat[1]=~/�ɤ���Ȥ�/){
			    print FIG "3\t";
			    print USER "3\t";
			}elsif($dat[1]=~/���ޤ����/){
			    print FIG "2\t";
			    print USER "2\t";
			}else{
			    print FIG "1\t";
			    print USER "1\t";
			}
## Question 3: cost
			if(!$dat[2]){
			    print USER "\t";
			}elsif($dat[2]=~/500�ʲ�/){
			    print USER "500�ʲ�\t";
			}elsif($dat[2]=~/500�ߤ���1000��/){
			    print USER "500�ߤ���1000��\t";
			}elsif($dat[2]=~/1000�ߤ���1500��/){
			    print USER "1000�ߤ���1500��\t";
			}elsif($dat[2]=~/1500�ߤ���2000��/){
			    print USER "1500�ߤ���2000��\t";
			}elsif($dat[2]=~/2000�߰ʾ�/){
			    print USER "2000�߰ʾ�\t";
			}else{
			    print USER "\t";
			}
## Question 4;��Degree of Satisfaction 
			if(!$dat[3]){
			    print FIG "\t";
			    print USER "\t";
			}elsif($dat[3]=~/������­/){
			    print FIG "5\t";
			    print USER "5\t";
			}elsif($dat[3]=~/�����­/){
			    print FIG "4\t";
			    print USER "4\t";
			}elsif($dat[3]=~/�ɤ���Ȥ�/){
			    print FIG "3\t";
			    print USER "3\t";
			}elsif($dat[3]=~/�������/){
			    print FIG "2\t";
			    print USER "2\t";
			}else{
			    print FIG "1\t";
			    print USER "1\t";
			}
## Question 5: Degree of modefied expectationradio
			if(!$dat[4]){
			    $subdat = "\t";
			}elsif($dat[4]=~/���Ԥ򤫤ʤ���ä�/){
			    $subdat = "2\t";
			}elsif($dat[4]=~/���Ԥ�����ä�/){
			    $subdat = "1\t";
			}elsif($dat[4]=~/�����̤�Ǥ��ä�/){
			    $subdat = "0\t";
			}elsif($dat[4]=~/���Ԥ��䲼��ä�/){
			    $subdat = "-1\t";
			}else{
			    $subdat = "-2\t";
			}
                        print FIG $subdat;
                        print USER $subdat;
## Question 6: Comment
			print FIG "$dat[5]\t";
			print USER "$dat[5]\t";
## date 2000-00-00 -
			print FIG "$dat[6]\n";
			print USER "$dat[6]\n";
# i/o file close
    close(IN);
    close(OUT);
    close(FIG);
    close(USER);
}
################################################
## ���Ͳ������ǡ��������̥ե������ʬ����
################################################
sub SubData
{
# input
    open(IN, "evaluation_number.dat") or die "can not open file\n";
    @data = <IN>; 
    close(IN); 
# output
    for($i=1;$i<7;$i++){
	$j = "OUT".$i;
	$k = "data_".$i.".dat";
    open($j, ">$k"); # 1 .. 6 file open
    }
    foreach(@data){
	chomp($_);
   	@subdata = split(/\t/, $_);
    for($i=1;$i<7;$i++){
	$j = "OUT".$i;
	$k = "data_".$i.".dat";
        if($subdata[1] =~ /$i/){
	print $j $subdata[0],$subdata[2],$subdata[4],$subdata[3],$subdata[5],$subdata[6],"\n";
    }else{}
    }
    }
    for($i=1;$i<7;$i++){
	$j = "OUT".$i;
    close($j);
    }
}
##########################################################
## ���֤�5��ʬ��˴��ԡ����ԤȤΥ��졢��­�٤�ʿ��ʬ����Ȥ�
########################################################
sub MeanVariance
{
# output
    open(OUT,">data_figure.gp");
# i���ܤΥǡ�������
    for($i=1;$i<7;$i++){ 
# var initialize
	for($k=1;$k<4;$k++){
	    $count[$k] = 0;
	    $x[$k] = 0;
	    $x_x[$k] = 0;
	    $mean[$k] = 0;
	    $mean_upper[$k] = 0;
	    $mean_lower[$k] = 0;
	    $mean_mean[$k] = 0;
	    $sd[$k] = 0;
	}
	$j = "IN".$i;
	$k = "data_".$i.".dat";
	open($j, "$k") or die "can not open file for writing\n"; # 1 .. 6 file open
	@data = <$j>; # i file load    
	close($j);
	foreach(@data){
	    chomp($_);
	    @subdata = split(/\t/, $_);
	        if(!$subdata[1] and !$subdata[2]){
                }else{
		    $subdata[2] += $subdata[1]; 
		} 
	    for($k=1;$k<4;$k++){ # k1:ex k2:mev k3:cs 
		if(!$subdata[$k]){ # number of data
		$count[$k] += 0; 
		}else{
		$count[$k] += 1;
	        }
		if(!$subdata[$k]){
		    $x[$k] +=  0;
		    $x_x[$k] += 0;
		}else{
		$x[$k] +=  $subdata[$k];
		$x_x[$k] += $subdata[$k]*$subdata[$k]; # square
	        }
	    }
	}
	# ʿ�Ѥ���(0�ǳ��ȥ��顼���Ф�)
	for($k=1;$k<4;$k++){
	    if(!$count[$k]){
		$mean[$k] = 0;
		$mean_mean[$k] = 0;
	    }else{
	    $mean[$k] = $x[$k]/$count[$k];
	    $mean_mean[$k] = $x_x[$k]/$count[$k];
	    $sq[$k] = sqrt($mean_mean[$k]-$mean[$k]*$mean[$k]);
	    $mean_upper[$k] = $mean[$k] + $sq[$k];
	    $mean_lower[$k] = $mean[$k] - $sq[$k];
	    }
	}
	$i_1=$i-0.28;
	$i_2=$i+0.28;
	print OUT $i, $i_1, $i_2, $count[1], $count[2], $count[3], $mean[1], $mean_upper[1], $mean_lower[1],$mean[2], $mean_upper[2], $mean_lower[2],$mean[3], $mean_upper[3], $mean_lower[3],"\n";
    }
    close(OUT);
}
#------------------ �����ޤ� --------------------------------------------------
