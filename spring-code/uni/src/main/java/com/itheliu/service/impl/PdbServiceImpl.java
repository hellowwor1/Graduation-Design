package com.itheliu.service.impl;

import com.itheliu.mapper.FubenMapper;
import com.itheliu.mapper.PdbMapper;
import com.itheliu.pojo.PDB;
import com.itheliu.pojo.Tiny;
import com.itheliu.service.PdbService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__04__22__-18:53
 */

@Service
public class PdbServiceImpl implements PdbService {
    @Autowired
    private PdbMapper pdbMapper;

    @Override
    public  PDB GetPdbByID(String id) {
        PDB pdb = pdbMapper.GetPdbByID(id);
        System.out.println(pdb);
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
        return pdb;
    }

}
