package com.example.newsindia.service;

import com.example.newsindia.model.NewsItem;
import java.io.InputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

@Service
public class RssNewsClient {

  private static final Logger logger = LoggerFactory.getLogger(RssNewsClient.class);
  private static final String USER_AGENT = "news-india-springboot/1.0 (Java HttpClient)";

  private final HttpClient httpClient;

  public RssNewsClient() {
    this.httpClient =
        HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(8))
            .followRedirects(HttpClient.Redirect.NORMAL)
            .build();
  }

  public List<NewsItem> fetchTopNews(String feedUrl, int limit) throws Exception {
    HttpRequest request =
        HttpRequest.newBuilder()
            .uri(URI.create(feedUrl))
            .header("User-Agent", USER_AGENT)
            .GET()
            .timeout(Duration.ofSeconds(15))
            .build();

    HttpResponse<InputStream> response =
        httpClient.send(request, HttpResponse.BodyHandlers.ofInputStream());

    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      throw new IllegalStateException("RSS HTTP status: " + response.statusCode());
    }

    try (InputStream in = response.body()) {
      return parseRss(in, limit);
    }
  }

  private List<NewsItem> parseRss(InputStream rssStream, int limit)
      throws ParserConfigurationException, java.io.IOException, SAXException {

    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    factory.setNamespaceAware(false);

    // Security hardening: avoid XXE / external entity resolution.
    factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
    factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
    factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
    factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
    factory.setXIncludeAware(false);
    factory.setExpandEntityReferences(false);

    Document doc = factory.newDocumentBuilder().parse(rssStream);
    NodeList itemNodes = doc.getElementsByTagName("item");

    List<NewsItem> items = new ArrayList<>();
    for (int i = 0; i < itemNodes.getLength() && items.size() < limit; i++) {
      Element item = (Element) itemNodes.item(i);

      String title = firstChildText(item, "title");
      String link = firstChildText(item, "link");
      String pubDate = firstChildText(item, "pubDate");

      if (title == null || title.isBlank()) {
        continue;
      }

      items.add(
          new NewsItem(
              title.trim(),
              link == null ? "" : link.trim(),
              pubDate == null ? "" : pubDate.trim()
          )
      );
    }

    logger.info("Parsed {} RSS items", items.size());
    return items;
  }

  private static String firstChildText(Element parent, String tagName) {
    NodeList nodes = parent.getElementsByTagName(tagName);
    if (nodes.getLength() == 0) {
      return null;
    }
    if (nodes.item(0).getTextContent() == null) {
      return null;
    }
    return nodes.item(0).getTextContent();
  }
}

