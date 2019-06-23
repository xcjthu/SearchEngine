package mypkg;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class ImageServer extends HttpServlet{
	public static final int PAGE_RESULT=10;
	public static final String indexDir="forIndex";
	public static final String picDir="";
	UserBean userBean;
	String keyword;

	public ImageServer(){
		super();
		userBean = new UserBean();
		keyword = "";
	}
	
	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.setContentType("text/html;charset=utf-8");
		request.setCharacterEncoding("utf-8");
		String queryString=request.getParameter("query");
		String pageString=request.getParameter("page");
		int page=1;
		if(pageString!=null){
			page=Integer.parseInt(pageString);
		}
		if(queryString==null){
			System.out.println("null query");
			//request.getRequestDispatcher("/Image.jsp").forward(request, response);
		}else{
			if(!keyword.equals(queryString)){
				userBean.SearchResult(queryString);
				keyword = queryString;
			}
			String[] contents = userBean.getContents(page);
			String[] titles = userBean.getTitles(page);
			String[] urls = userBean.getUrls(page);
			int len = userBean.getLen(page);
			String formUrl = userBean.getFormUrl();
			String retInfo = userBean.getRetInfo();
			String[] pictureUrls = userBean.getPictureUrls(page);
			double[] pageRanks = userBean.getPageRanks(page);
			double[] pageScores = userBean.getPageScores(page);
			request.setAttribute("currentQuery",queryString);
			request.setAttribute("currentPage", page);
			request.setAttribute("Contents", contents);
			request.setAttribute("Titles", titles);
			request.setAttribute("Urls", urls);
			request.setAttribute("FormUrl", formUrl);
			request.setAttribute("RetInfo", retInfo);
			request.setAttribute("PageRanks", pageRanks);
			request.setAttribute("PageScores", pageScores);
			request.setAttribute("Len", len);
			request.setAttribute("PictureUrls", pictureUrls);
			request.getRequestDispatcher("/result.jsp").forward(request,
					response);
		}
	}

	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		this.doGet(request, response);
	}
}
