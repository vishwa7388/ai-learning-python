package com.example.newsindia.model;

import java.util.List;

public record NewsResponse(
    List<NewsItem> items,
    String message
) {}

