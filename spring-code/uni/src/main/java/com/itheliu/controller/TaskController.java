package com.itheliu.controller;

import com.itheliu.pojo.PageBean;
import com.itheliu.pojo.Result;
import com.itheliu.pojo.Task;
import com.itheliu.pojo.fuben;
import com.itheliu.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__05__05__-21:48
 */

@RestController
@RequestMapping("/monitor")
public class TaskController {

    @Autowired
    private TaskService taskService;



    @PostMapping("/prediction-tasks")
    public Result<List<Task>> list(
    ){
        List<Task> all = taskService.getAll();
        System.out.println("时间:"+all);
        return  Result.success(all);
    }
}
