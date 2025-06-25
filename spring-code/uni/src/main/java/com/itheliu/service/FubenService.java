package com.itheliu.service;

import com.itheliu.pojo.PDB;
import com.itheliu.pojo.PageBean;
import com.itheliu.pojo.fuben;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__01__21__-16:17
 */
public interface FubenService {
    //分页列表查询
    PageBean<fuben> List(Integer pageNum, Integer pageSize);

    fuben GetByID(String id);

    PageBean<fuben> MhcList(Integer pageNum, Integer pageSize);

    List<PDB> GetPdbsByID(String id);
}
