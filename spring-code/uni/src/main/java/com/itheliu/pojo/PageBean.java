package com.itheliu.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__01__21__-17:27
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PageBean<T> {
    private Long total;//总条数
    private List<T> items;//当前页面集合
}
