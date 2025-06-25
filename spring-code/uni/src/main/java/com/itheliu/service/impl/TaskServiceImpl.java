package com.itheliu.service.impl;
import com.itheliu.mapper.TaskMapper;
import com.itheliu.pojo.Task;
import com.itheliu.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__05__05__-16:49
 */
@Service
public class TaskServiceImpl implements TaskService {
    @Autowired
    private TaskMapper taskMapper;


    @Override
    public List<Task> getAll() {
        List<Task> all = taskMapper.getAll();

        return all;
    }
}
