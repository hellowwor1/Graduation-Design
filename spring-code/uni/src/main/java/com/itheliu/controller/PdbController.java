package com.itheliu.controller;

import com.itheliu.mapper.PdbMapper;
import com.itheliu.pojo.PDB;
import com.itheliu.pojo.PageBean;
import com.itheliu.pojo.Result;
import com.itheliu.pojo.fuben;
import com.itheliu.service.FubenService;
import com.itheliu.service.PdbService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/Pdb")
public class PdbController {

    @Autowired
    private PdbService pdbService;

    @GetMapping("/detail/{id}")
    public Result<PDB> getPdb(@PathVariable String id) {
        // 根据 ID 获取副本数据的Pdbs

        PDB pdb = pdbService.GetPdbByID(id);

        System.out.println(pdb);
        return Result.success(pdb);
    }


}