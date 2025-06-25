package com.itheliu.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author hellowwor1
 * @create 2025__01__21__-16:25
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class Result<T> {
    private Integer code;//业务状态码
    private String message;//提示信息
    private T data;//响应数据


    //带响应的数据
    public  static <E> Result<E> success(E data){
        return  new Result<>(0,"操作成功",data);
    }
    //不带响应数据
    public  static Result success(){return new Result(0,"操作成功",null);}

    public  static Result error(String message){return new Result(1,message,null);}
}
