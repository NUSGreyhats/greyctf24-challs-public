(module
 (type $0 (func (param i32 i32) (result i32)))
 (import "env" "memory" (memory $0 0))
 (export "levenshtein" (func $assembly/index/levenshtein))
 (export "memory" (memory $0))
 (func $assembly/index/levenshtein (param $0 i32) (param $1 i32) (result i32)
  (local $2 i32)
  (local $3 i32)
  (local $4 i32)
  (local $5 i32)
  (local $6 i32)
  (local $7 i32)
  (local $8 i32)
  (local $9 i32)
  (local $10 i32)
  (local $11 i32)
  (local $12 i32)
  (local $13 i32)
  (local $14 i32)
  (local $15 i32)
  (local $16 i32)
  (local $17 i32)
  (local $18 i32)
  loop $while-continue|0
   local.get $0
   if (result i32)
    local.get $0
    i32.const 1
    i32.sub
    i32.load8_u
    local.get $1
    i32.load8_u offset=99
    i32.eq
   else
    i32.const 0
   end
   if
    local.get $0
    i32.const 1
    i32.sub
    local.set $0
    local.get $1
    i32.const 1
    i32.sub
    local.set $1
    br $while-continue|0
   end
  end
  loop $while-continue|1
   local.get $0
   local.get $18
   i32.gt_u
   if (result i32)
    local.get $18
    i32.load8_u
    local.get $18
    i32.load8_u offset=100
    i32.eq
   else
    i32.const 0
   end
   if
    local.get $18
    i32.const 1
    i32.add
    local.set $18
    br $while-continue|1
   end
  end
  local.get $0
  local.get $18
  i32.sub
  local.tee $3
  i32.eqz
  local.get $1
  local.get $18
  i32.sub
  local.tee $15
  i32.const 3
  i32.lt_u
  i32.or
  if
   i32.const 0
   return
  end
  i32.const -1
  local.set $17
  loop $for-loop|2
   local.get $7
   local.get $3
   i32.const 1
   i32.shl
   i32.lt_u
   if
    local.get $7
    i32.const 2
    i32.shl
    local.get $4
    i32.const 1
    i32.add
    local.tee $0
    i32.store offset=200
    local.get $7
    i32.const 1
    i32.add
    local.tee $1
    i32.const 1
    i32.add
    local.set $7
    local.get $1
    i32.const 2
    i32.shl
    local.get $4
    local.get $18
    i32.add
    i32.load8_u
    i32.store offset=200
    local.get $0
    local.set $4
    br $for-loop|2
   end
  end
  local.get $3
  i32.const 1
  i32.shl
  i32.const 1
  i32.sub
  local.set $14
  loop $while-continue|3
   local.get $2
   local.get $15
   i32.const 3
   i32.sub
   i32.lt_u
   if
    local.get $18
    local.get $2
    local.tee $0
    i32.add
    i32.load8_u offset=100
    local.set $13
    local.get $0
    i32.const 1
    i32.add
    local.tee $7
    local.get $18
    i32.add
    i32.load8_u offset=100
    local.set $12
    local.get $0
    i32.const 2
    i32.add
    local.tee $8
    local.get $18
    i32.add
    i32.load8_u offset=100
    local.set $11
    local.get $0
    i32.const 3
    i32.add
    local.tee $1
    local.get $18
    i32.add
    i32.load8_u offset=100
    local.set $10
    local.get $0
    i32.const 4
    i32.add
    local.tee $2
    local.set $17
    i32.const 0
    local.set $4
    loop $for-loop|4
     local.get $4
     local.get $14
     i32.lt_u
     if
      local.get $4
      i32.const 1
      i32.add
      i32.const 2
      i32.shl
      i32.load offset=200
      local.set $16
      local.get $1
      local.get $17
      i32.gt_s
      local.set $9
      local.get $1
      local.set $6
      local.get $8
      local.set $5
      local.get $4
      i32.const 2
      i32.shl
      local.tee $8
      i32.load offset=200
      local.tee $3
      local.get $0
      i32.lt_s
      local.get $7
      local.tee $1
      local.get $0
      i32.lt_s
      i32.or
      if (result i32)
       local.get $7
       i32.const 1
       i32.add
       local.get $3
       i32.const 1
       i32.add
       local.get $3
       local.get $7
       i32.gt_s
       select
      else
       local.get $0
       local.get $0
       i32.const 1
       i32.add
       local.get $13
       local.get $16
       i32.eq
       select
      end
      local.set $7
      local.get $8
      local.get $9
      local.get $1
      local.get $5
      i32.gt_s
      local.get $1
      local.get $7
      i32.gt_s
      i32.or
      if (result i32)
       local.get $5
       i32.const 1
       i32.add
       local.get $7
       i32.const 1
       i32.add
       local.get $5
       local.get $7
       i32.lt_s
       select
      else
       local.get $1
       local.get $1
       i32.const 1
       i32.add
       local.get $12
       local.get $16
       i32.eq
       select
      end
      local.tee $8
      local.get $5
      i32.lt_s
      local.get $5
      local.get $6
      i32.gt_s
      i32.or
      if (result i32)
       local.get $6
       i32.const 1
       i32.add
       local.get $8
       i32.const 1
       i32.add
       local.get $6
       local.get $8
       i32.lt_s
       select
      else
       local.get $5
       local.get $5
       i32.const 1
       i32.add
       local.get $11
       local.get $16
       i32.eq
       select
      end
      local.tee $1
      local.get $6
      i32.lt_s
      i32.or
      if (result i32)
       local.get $17
       i32.const 1
       i32.add
       local.get $1
       i32.const 1
       i32.add
       local.get $1
       local.get $17
       i32.gt_s
       select
      else
       local.get $6
       local.get $6
       i32.const 1
       i32.add
       local.get $10
       local.get $16
       i32.eq
       select
      end
      local.tee $17
      i32.store offset=200
      local.get $3
      local.set $0
      local.get $4
      i32.const 2
      i32.add
      local.set $4
      br $for-loop|4
     end
    end
    br $while-continue|3
   end
  end
  loop $while-continue|5
   local.get $2
   local.get $15
   i32.lt_u
   if
    local.get $18
    local.get $2
    local.tee $0
    i32.add
    i32.load8_u offset=100
    local.set $6
    local.get $0
    i32.const 1
    i32.add
    local.tee $2
    local.set $17
    i32.const 0
    local.set $4
    loop $for-loop|6
     local.get $4
     local.get $14
     i32.lt_u
     if
      local.get $4
      i32.const 1
      i32.add
      i32.const 2
      i32.shl
      i32.load offset=200
      local.set $5
      local.get $4
      i32.const 2
      i32.shl
      local.tee $3
      i32.load offset=200
      local.tee $1
      local.get $0
      i32.lt_s
      local.get $0
      local.get $17
      i32.gt_s
      i32.or
      if (result i32)
       local.get $17
       i32.const 1
       i32.add
       local.get $1
       i32.const 1
       i32.add
       local.get $1
       local.get $17
       i32.gt_s
       select
      else
       local.get $0
       local.get $0
       i32.const 1
       i32.add
       local.get $5
       local.get $6
       i32.eq
       select
      end
      local.set $17
      local.get $3
      local.get $17
      i32.store offset=200
      local.get $1
      local.set $0
      local.get $4
      i32.const 2
      i32.add
      local.set $4
      br $for-loop|6
     end
    end
    br $while-continue|5
   end
  end
  i32.const 0
 )
)
