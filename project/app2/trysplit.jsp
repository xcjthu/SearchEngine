<%@page language="java" contentType="text/html" pageEncoding="UTF-8" %>
<!DOCTYPE HTML >
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>肖特搜索引擎</title>
  <link rel="stylesheet" type="text/css" href="css/style.css" />
</head>
<STYLE>
</STYLE>
<body>
  <form method="get">
    <input   value="${sl}" type="text" id="sl" name="sl">
    <input type="submit" value="submit">
  </form>
  
  <%
  String value = request.getParameter("sl");
  if(value != null){
  for(int i=0; i<Integer.valueOf(value); i++)
    {
    out.print("<tr>");out.print("<td ><input id='sl' type='text'> ");out.print("</td>");out.print("</tr>");
    }
  }
  %>
<body>
</html>

