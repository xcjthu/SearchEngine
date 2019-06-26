<%@page language="java" contentType="text/html" pageEncoding="UTF-8" %>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>

<!DOCTYPE HTML >
<html>
<head>
  <base href="<%=basePath%>">

  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>肖特搜索引擎</title>
  <link rel="stylesheet" type="text/css" href="css/style.css" />
</head>
<STYLE>
</STYLE>
<body>
  <div class="dropdown">
    <button class="dropbtn">下拉菜单</button>
    <div class="dropdown-content">
      <a href="index.jsp">文字搜索</a>
    </div>
  </div>
  <div class="SearchBlock">
    <!-- <h1 class="SearchTitle">肖特 Search Engine</h1> -->
    <img class="IndexImage" src="img/imagebackground.png" alt="肖特搜索引擎" />
    <form id="form1" name="form1" method="get" action="servlet/ImageSearchServer">
      <input type="search" name="query" style="text-align: left; width: 500px; height: 40px;font-size: 20px">
      <input type="submit" value="搜图" style="background-color: #007fff; text-align: center; width: 100px; height: 40px;font-size: 20px; color: white; border: none">
    </form>

  <!-- <img src="http://www.w3school.com.cn/i/eg_tulip.jpg"  alt="上海鲜花港 - 郁金香" /> -->
  </div>
<body>
</html>