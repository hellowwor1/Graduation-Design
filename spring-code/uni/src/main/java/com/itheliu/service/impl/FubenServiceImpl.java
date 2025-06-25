package com.itheliu.service.impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.itheliu.mapper.FubenMapper;
import com.itheliu.mapper.PdbMapper;
import com.itheliu.pojo.PDB;
import com.itheliu.pojo.PageBean;
import com.itheliu.pojo.Tiny;
import com.itheliu.pojo.fuben;
import com.itheliu.service.FubenService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__01__21__-16:18
 */
@Service
public class FubenServiceImpl implements FubenService {

    @Autowired
    private FubenMapper fubenMapper;


    @Autowired
    private PdbMapper pdbMapper;

    @Override
    public PageBean<fuben> List(Integer pageNum, Integer pageSize) {
        //创建PagenBean对象
        PageBean<fuben> pb = new PageBean<>();

        //开启分页查询 PageHelper
        PageHelper.startPage(pageNum, pageSize);

        //调用mapper
        List<fuben> as = fubenMapper.List();
//        System.out.println(as);

        Page<fuben> p = (Page<fuben>) as;

        //最后把数据填充进去
        pb.setTotal(p.getTotal());
        pb.setItems(p.getResult());
        return pb;
    }

    @Override
    public fuben GetByID(String id) {
        fuben fuben = fubenMapper.GetById(id);
        return fuben;
    }

    @Override
    public PageBean<fuben> MhcList(Integer pageNum, Integer pageSize) {
        //创建PagenBean对象
        PageBean<fuben> pb = new PageBean<>();

        //开启分页查询 PageHelper
        PageHelper.startPage(pageNum, pageSize);

        //调用mapper
        List<fuben> as = fubenMapper.MhcList();
//        System.out.println(as);

        Page<fuben> p = (Page<fuben>) as;

        //最后把数据填充进去
        pb.setTotal(p.getTotal());
        pb.setItems(p.getResult());
        return pb;
    }

    @Override
    public List<PDB> GetPdbsByID(String id) {
        List<PDB> pdbs = pdbMapper.GetByFubenId(id);
        for (PDB pdb : pdbs) {
            String startIndex = pdb.getStartIndex();
            String endIndex = pdb.getEndIndex();
            String chain = pdb.getChain();
            String[] startIndexSplit = startIndex.split(",");
            String[] endIndexSplit = endIndex.split(",");
            String[] chainSplit = chain.split(",");
            List<Tiny> tiny =new ArrayList<>();
            for(int i=0;i<chainSplit.length;i++){
                tiny.add(new Tiny(startIndexSplit[i],endIndexSplit[i],chainSplit[i]));
            }
            pdb.setTiny(tiny);
        }

        return pdbs;
    }
}
