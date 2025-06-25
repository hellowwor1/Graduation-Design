package com.itheliu.mapper;

import com.itheliu.pojo.fuben;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__01__21__-16:18
 */
@Mapper
public interface FubenMapper {
    List<fuben> List();
    List<fuben> MhcList();
    fuben  GetById(String id);
}
