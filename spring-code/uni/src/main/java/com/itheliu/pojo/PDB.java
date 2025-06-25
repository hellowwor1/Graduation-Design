package com.itheliu.pojo;

import lombok.Data;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__01__20__-17:03
 */
@Data
public class PDB {
    private Integer pid;
    private String pdbId;
    private String method;
    private double accuracy;
    private String subunit;
    private String startIndex;
    private String endIndex;
    private String chain;
    private String id;
    private Integer hasTiny;

    //在服务器加上去的字段
    private List<Tiny> tiny;
}
