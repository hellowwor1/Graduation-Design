package com.itheliu.mapper;

import com.itheliu.pojo.PDB;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * @author hellowwor1
 * @create 2025__04__17__-15:00
 */

@Mapper
public interface PdbMapper {

    List<PDB> GetByFubenId(String id);


    PDB GetPdbByID(String pdb_id);
}
