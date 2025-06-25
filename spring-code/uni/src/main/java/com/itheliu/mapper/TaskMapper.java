package com.itheliu.mapper;

import com.itheliu.pojo.Task;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__05__05__-16:50
 */
@Mapper
public interface TaskMapper {
    List<Task> getAll();
}
