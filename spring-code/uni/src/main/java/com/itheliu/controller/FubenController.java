package com.itheliu.controller;

import com.itheliu.pojo.PDB;
import com.itheliu.pojo.PageBean;
import com.itheliu.pojo.Result;
import com.itheliu.pojo.fuben;
import com.itheliu.service.FubenService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__01__21__-16:19
 */
@RestController
@RequestMapping("/fuben")
public class FubenController {

        @Autowired
        private FubenService fubenService;

        @GetMapping("/getAll")
        public Result<PageBean<fuben>> list( Integer pageNum,
                Integer pageSize
        ){
              PageBean<fuben>pb=fubenService.List(pageNum,pageSize);
              return  Result.success(pb);
        }

    @GetMapping("/get_mhcAll")
    public Result<PageBean<fuben>> mhc_list( Integer pageNum,
                                         Integer pageSize
    ){
        PageBean<fuben>pb=fubenService.MhcList(pageNum,pageSize);
        return  Result.success(pb);
    }

    @GetMapping("/detail/{id}")
    public Result<fuben> getFubenDetail(@PathVariable String id) {
        // 根据 ID 获取副本数据
        fuben fuben = fubenService.GetByID(id);
        System.out.println(fuben);
        return  Result.success(fuben);
    }


    @GetMapping("/detail/{id}/pdbs")
    public Result<List<PDB>> getFubenPdbs(@PathVariable String id) {
        // 根据 ID 获取副本数据的Pdbs

        List<PDB> pdbs = fubenService.GetPdbsByID(id);

        System.out.println(pdbs);
        return Result.success(pdbs);
    }


}

