package com.itheliu.pojo;

import lombok.Data;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__05__05__-23:40
 */
@Data
public class MethodResult {
        private int code;
        private String method;
        private String status;
        private List<RankingItem> ranking;

}
