package com.itheliu.pojo;
import com.fasterxml.jackson.annotation.JsonRawValue;
import lombok.Data;


/**
 * @author hellowwor1
 * @create 2025__05__05__-16:42
 */
@Data
public class Task {
     private String taskId;
     private String fileName;
     private String status;
     private String createTime;
     private Integer progress;

     @JsonRawValue
     private String result;
}

